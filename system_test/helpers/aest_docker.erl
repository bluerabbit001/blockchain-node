-module(aest_docker).

%=== EXPORTS ===================================================================

%% API exports
-export([start/1]).
-export([stop/1]).
-export([prepare_spec/2]).
-export([peer_from_spec/2]).
-export([setup_node/2]).
-export([delete_node/1]).
-export([start_node/1]).
-export([stop_node/2]).
-export([kill_node/1]).
-export([node_logs/1]).
-export([get_peer_address/1]).
-export([get_service_address/2]).
-export([extract_archive/3]).
-export([run_cmd_in_node_dir/2]).

%=== MACROS ====================================================================

-define(CONFIG_FILE_TEMPLATE, "epoch.yaml.mustache").
-define(EPOCH_CONFIG_FILE, "/home/epoch/epoch.yaml").
-define(EPOCH_LOG_FOLDER, "/home/epoch/node/log").
-define(EPOCH_KEYS_FOLDER, "/home/epoch/node/keys").
-define(EPOCH_MINE_RATE, 1000).
-define(EXT_HTTP_PORT, 3013).
-define(EXT_SYNC_PORT, 3015).
-define(INT_HTTP_PORT, 3113).
-define(INT_WS_PORT, 3114).
-define(EPOCH_STOP_TIMEOUT, 30).
-define(PEER_KEYS_PASSWORD, <<"top secret">>).

%=== TYPES =====================================================================

-type log_fun() :: fun((io:format(), list()) -> ok) | undefined.
-type test_uid() :: binary() | undefined.
-type service_label() :: ext_http | int_http | int_ws.

%% State of the docker backend
-type backend_state() :: #{
    postfix := binary(),        % A unique postfix to add to container names.
    log_fun := log_fun(),       % Function to use for logging.
    data_dir := binary(),       % The directory where the templates can be found.
    temp_dir := binary(),       % A temporary directory that can be used to generate
                                % configuration files and save the log files.
    net_id := binary()          % Docker network identifier
}.

%% Node specification
-type node_spec() :: #{
    name := atom(),
    pubkey => binary(),         % Public part of the peer key
    privkey => binary(),        % Private part of the peer key
    peers := [binary()],        % URLs of the peer nodes
    source := {pull, binary()}, % Source of the node image
    mine_rate => default | pos_integer(),
    hard_forks => #{non_neg_integer() => non_neg_integer()} % Consensus protocols (version -> height)
}.

%% State of a node
-type node_state() :: #{
    spec := node_spec(),        % Backup of the spec used when adding the node
    log_fun := log_fun(),       % Function to use for logging
    hostname := atom(),         % Hostname of the container running the node
    pubkey := binary(),         % Public part of the peer key
    privkey := binary(),        % Private part of the peer key
    exposed_ports := #{service_label() => pos_integer()},
    local_ports := #{service_label() => pos_integer()}
}.

-type start_options() :: #{
    test_id => test_uid(),
    log_fun => log_fun(),
    data_dir := binary(),
    temp_dir := binary()
}.

-type stop_node_options() :: #{
    soft_timeout => pos_integer() | infinity,
    hard_timeout => pos_integer()
}.


%=== GENERIC API FUNCTIONS =====================================================

-spec start(start_options()) -> backend_state().
start(Options) ->
    TestId = maps:get(test_id, Options),
    Postfix = uid2postfix(TestId),
    LogFun = maps:get(log_fun, Options),
    {ok, DataDir} = maps:find(data_dir, Options),
    {ok, TempDir} = maps:find(temp_dir, Options),
    ok = aest_docker_api:start(),
    NetName = <<"epoch", Postfix/binary>>,
    #{'Id' := NetId} = aest_docker_api:create_network(#{name => NetName}),
    log(LogFun, "Network ~p [~s] created", [NetName, NetId]),
    #{postfix => Postfix,
      log_fun => LogFun,
      data_dir => DataDir,
      temp_dir => TempDir,
      net_id => NetId
    }.

-spec stop(backend_state()) -> ok.
stop(BackendState) ->
    aest_docker_api:prune_networks(),
    log(BackendState, "Networks pruned", []),
    ok.

-spec prepare_spec(node_spec(), backend_state()) -> node_spec().
prepare_spec(#{pubkey := PubKey, privkey := PrivKey} = Spec, BackendState) ->
    #{data_dir := DataDir} = BackendState,
    #{name := Name} = Spec,
    KeysDir = keys_dir(DataDir, Name),
    Password = ?PEER_KEYS_PASSWORD,
    {PubFile, PrivFile} = aec_keys:peer_key_filenames(KeysDir),
    file:delete(PubFile),
    file:delete(PrivFile),
    aec_keys:save_peer_keys(Password, KeysDir, PubKey, PrivKey),
    Spec;
prepare_spec(#{pubkey := _PubKey}, _BackendState) ->
    error(pubkey_without_privkey);
prepare_spec(#{privkey := _PrivKey}, _BackendState) ->
    error(provkey_without_pubkey);
prepare_spec(Spec, BackendState) ->
    #{data_dir := DataDir} = BackendState,
    #{name := Name} = Spec,
    Password = ?PEER_KEYS_PASSWORD,
    KeysDir = keys_dir(DataDir, Name),
    {_, PeerPub, _, PeerPriv} = aec_keys:setup_peer_keys(Password, KeysDir),
    Spec#{pubkey => PeerPub, privkey => PeerPriv}.

-spec peer_from_spec(node_spec(), backend_state()) -> binary().
peer_from_spec(Spec, BackendState) ->
    #{postfix := Postfix} = BackendState,
    #{name := Name, pubkey := Key} = Spec,
    Hostname = format("~s~s", [Name, Postfix]),
    aec_peers:encode_peer_address(
        #{host => Hostname, port => ?EXT_SYNC_PORT, pubkey => Key}).

-spec setup_node(node_spec(), backend_state()) -> node_spec().
setup_node(Spec, BackendState) ->
    #{log_fun := LogFun,
      postfix := Postfix,
      data_dir := DataDir,
      temp_dir := TempDir,
      net_id := NetId} = BackendState,
    #{name := Name,
      pubkey := PubKey,
      privkey := PrivKey,
      peers := Peers,
      source := {pull, Image}} = Spec,
    MineRate = maps:get(mine_rate, Spec, ?EPOCH_MINE_RATE),

    Hostname = format("~s~s", [Name, Postfix]),
    ExposedPorts = #{
        sync => ?EXT_SYNC_PORT,
        ext_http => ?EXT_HTTP_PORT,
        int_http => ?INT_HTTP_PORT,
        int_ws => ?INT_WS_PORT
    },
    LocalPorts = allocate_ports([sync, ext_http, int_http, int_ws]),
    NodeState = #{
        spec => spec,
        log_fun => LogFun,
        name => Name,
        hostname => Hostname,
        pubkey => PubKey,
        privkey => PrivKey,
        exposed_ports => ExposedPorts,
        local_ports => LocalPorts
    },

    ConfigFileName = format("epoch_~s.yaml", [Name]),
    ConfigFilePath = filename:join([TempDir, "config", ConfigFileName]),
    TemplateFile = filename:join(DataDir, ?CONFIG_FILE_TEMPLATE),
    PeerVars = lists:map(fun (Addr) -> #{peer => Addr} end, Peers),
    ct:log("PeerVars: ~p", [PeerVars]),
    HardForkVars =
        case maps:find(hard_forks, Spec) of
            error -> #{};
            {ok, HardForks} ->
                #{hard_forks_present => [#{}],
                  hard_forks =>
                      lists:map(fun({V, H}) -> #{version => V, height => H} end,
                                maps:to_list(HardForks))}
        end,
    ct:log("HardForkVars: ~p", [HardForkVars]),
    RootVars = HardForkVars#{
        hostname => Name,
        ext_addr => format("http://~s:~w/", [Hostname, ?EXT_HTTP_PORT]),
        peers => PeerVars,
        key_password => ?PEER_KEYS_PASSWORD,
        services => #{
            sync => #{port => ?EXT_SYNC_PORT},
            ext_http => #{port => ?EXT_HTTP_PORT},
            int_http => #{port => ?INT_HTTP_PORT},
            int_ws => #{port => ?INT_WS_PORT}
        }
    },
    Context = #{epoch_config => RootVars},
    ok = write_template(TemplateFile, ConfigFilePath, Context),
    Command =
        case MineRate of
            default -> [];
            _ when is_integer(MineRate), MineRate > 0 ->
                ["-aecore", "expected_mine_rate", MineRate]
        end,
    LogPath = filename:join(TempDir, format("~s_logs", [Name])),
    ok = filelib:ensure_dir(filename:join(LogPath, "DUMMY")),
    KeysDir = keys_dir(DataDir, Name),
    PortMapping = maps:fold(fun(Label, Port, Acc) ->
        [{tcp, maps:get(Label, LocalPorts), Port} | Acc]
    end, [], ExposedPorts),
    DockerConfig = #{
        hostname => Hostname,
        network => NetId,
        image => Image,
        ulimits => [{nofile, 1024, 1024}],
        command => Command,
        env => #{"EPOCH_CONFIG" => ?EPOCH_CONFIG_FILE},
        volumes => [
            {rw, KeysDir, ?EPOCH_KEYS_FOLDER},
            {ro, ConfigFilePath, ?EPOCH_CONFIG_FILE},
            {rw, LogPath, ?EPOCH_LOG_FOLDER}
        ],
        ports => PortMapping
    },
    #{'Id' := ContId} = aest_docker_api:create_container(Hostname, DockerConfig),
    log(NodeState, "Container ~p [~s] created", [Name, ContId]),
    NodeState#{
        container_name => Hostname,
        container_id => ContId,
        config_path => ConfigFilePath
    }.

-spec delete_node(node_state()) -> ok.
delete_node(#{container_id := ID, hostname := Name} = NodeState) ->
    aest_docker_api:delete_container(ID),
    log(NodeState, "Container ~p [~s] deleted", [Name, ID]),
    ok.

-spec start_node(node_state()) -> node_state().
start_node(#{container_id := ID, hostname := Name} = NodeState) ->
    aest_docker_api:start_container(ID),
    log(NodeState, "Container ~p [~s] started", [Name, ID]),
    NodeState.

-spec stop_node(node_state(), stop_node_options()) -> node_state().
stop_node(#{container_id := ID, hostname := Name} = NodeState, Opts) ->
    Timeout = maps:get(soft_timeout, Opts, ?EPOCH_STOP_TIMEOUT),
    TimeoutMs = case Timeout of infinity -> infinity; _ -> Timeout * 1000 end,
    case is_running(ID) of
        false ->
            log(NodeState, "Container ~p [~s] already not running", [Name, ID]);
        true ->
            attempt_epoch_stop(NodeState, TimeoutMs),
            case wait_stopped(ID, Timeout) of %% TODO Fix this call that has timeout actual parameter as seconds but handled inside function definition as milliseconds.
                timeout ->
                    aest_docker_api:stop_container(ID, Opts);
                ok ->
                    log(NodeState,
                        "Container ~p [~s] detected as stopped", [Name, ID]),
                    ok
            end,
            log(NodeState, "Container ~p [~s] stopped", [Name, ID])
    end,
    NodeState.

-spec kill_node(node_state()) -> node_state().
kill_node(#{container_id := ID, hostname := Name} = NodeState) ->
    aest_docker_api:kill_container(ID),
    log(NodeState, "Container ~p [~s] killed", [Name, ID]),
    NodeState.

-spec node_logs(node_state()) -> iodata().
node_logs(#{container_id := ID} = _NodeState) ->
    aest_docker_api:container_logs(ID).

-spec get_peer_address(node_state()) -> binary().
get_peer_address(NodeState) ->
    #{hostname := Hostname,
      exposed_ports := #{sync := Port},
      sync_pubkey := Key} = NodeState,
    aec_peers:encode_peer_address(#{host => Hostname,
                                    port => Port,
                                    pubkey => Key}).

-spec get_service_address(service_label(), node_state()) -> binary().
get_service_address(sync, NodeState) ->
    #{local_ports := #{sync := Port}, pubkey := Key} = NodeState,
    aec_peers:encode_peer_address(#{host => <<"localhost">>,
                                    port => Port,
                                    pubkey => Key});
get_service_address(Service, NodeState)
  when Service == ext_http; Service == int_http ->
    #{local_ports := #{Service := Port}} = NodeState,
    format("http://localhost:~w/", [Port]);
get_service_address(int_ws, NodeState) ->
    #{local_ports := #{int_ws := Port}} = NodeState,
    format("ws://localhost:~w/", [Port]).

extract_archive(#{container_id := ID, hostname := Name} = NodeState, Path, Archive) ->
    ok = aest_docker_api:extract_archive(ID, Path, Archive),
    log(NodeState, "Extracted archive of size ~p in container ~p [~s] at path ~p", [byte_size(Archive), Name, ID, Path]),
    NodeState.

run_cmd_in_node_dir(#{container_id := ID, hostname := Name} = NodeState, Cmd) ->
    log(NodeState, "Running command ~p on container ~p [~s]", [Cmd, Name, ID]),
    Cmd1 = lists:flatten(io_lib:format("docker exec ~s ~s", [ID, lists:join($ , Cmd)])),
    Result = lib:nonl(os:cmd(Cmd1)),
    log(NodeState, "Run command ~p on container ~p [~s] with result ~p", [Cmd, Name, ID, Result]),
    {ok, Result, NodeState}.

%=== INTERNAL FUNCTIONS ========================================================

keys_dir(DataDir, Name) ->
    KeysDir = filename:join([DataDir, "keys", Name]),
    ok = filelib:ensure_dir(filename:join(KeysDir, "DUMMY")),
    KeysDir.

log(#{log_fun := LogFun}, Fmt, Args) -> log(LogFun, Fmt, Args);
log(undefined, _Fmt, _Args) -> ok;
log(LogFun, Fmt, Args) when is_function(LogFun) -> LogFun(Fmt, Args).

uid2postfix(undefined) -> <<>>;
uid2postfix(<<>>) -> <<>>;
uid2postfix(Uid) -> <<"_", Uid/binary>>.

free_port() ->
    {ok, Socket} = gen_tcp:listen(0, [{reuseaddr, true}]),
    {ok, Port} = inet:port(Socket),
    gen_tcp:close(Socket),
    Port.

allocate_ports(Labels) -> allocate_ports(Labels, #{}).

allocate_ports([], Acc) -> Acc;
allocate_ports([Label | Labels], Acc) ->
    allocate_ports(Labels, Acc#{Label => free_port()}).


format(Fmt, Args) ->
    iolist_to_binary(io_lib:format(Fmt, Args)).

write_template(TemplateFile, OutputFile, Context) ->
    {{ok, TemplateBin}, _} = {file:read_file(TemplateFile), TemplateFile},
    Data = bbmustache:render(TemplateBin, Context, [{key_type, atom}]),
    ok = filelib:ensure_dir(OutputFile),
    file:write_file(OutputFile, Data).

wait_stopped(Id, Timeout) -> wait_stopped(Id, Timeout, os:timestamp()).

wait_stopped(Id, Timeout, StartTime) ->
    case is_running(Id) of
        false -> ok;
        true -> maybe_continue_waiting(Id, Timeout, StartTime)
    end.

is_running(Id) -> is_running(Id, 5).

is_running(_Id, 0) -> error(retry_exausted);
is_running(Id, Retries) ->
    case aest_docker_api:inspect(Id) of
        #{'State' := State} -> maps:get('Running', State, false);
        _ ->
            % Inspect may fail sometime when stopping a node, just retry
            timer:sleep(100),
            is_running(Id, Retries - 1)
    end.

attempt_epoch_stop(#{container_id := ID, hostname := Name} = NodeState, Timeout) ->
    Cmd = ["/home/epoch/node/bin/epoch", "stop"],
    CmdStr = lists:join($ , Cmd),
    log(NodeState,
        "Container ~p [~s] still running: "
        "attempting to stop node by executing command ~s",
        [Name, ID, CmdStr]),
    try
        {ok, _} = aest_docker_api:exec(ID, Cmd, #{timeout => Timeout}),
        log(NodeState, "Command executed on container ~p [~s]: ~s",
            [Name, ID, CmdStr])
    catch
        throw:{exec_start_timeout, TimeoutInfo} ->
            log(NodeState,
                "Command execution timed out on container ~p [~s]:~n~p",
                [Name, ID, TimeoutInfo])
    end,
    ok.

maybe_continue_waiting(Id, infinity, StartTime) ->
    timer:sleep(100),
    wait_stopped(Id, infinity, StartTime);
maybe_continue_waiting(Id, Timeout, StartTime) ->
    case timer:now_diff(os:timestamp(), StartTime) > (1000 * Timeout) of
        true -> timeout;
        false ->
            timer:sleep(200),
            wait_stopped(Id, Timeout, StartTime)
    end.
