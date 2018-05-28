-module(aesc_session_noise).
-behaviour(gen_server).

-include("aesc_codec.hrl").

-export([connect/3
       , accept/2
       , close/1]).

-export([channel_open/2
       , channel_accept/2
       , funding_created/2
       , funding_signed/2
       , funding_locked/2
       , deposit_created/2
       , deposit_signed/2
       , deposit_locked/2
       , channel_reestablish/2
       , update/2
       , update_ack/2
       , update_error/2
       , dep_created/2
       , dep_signed/2
       , dep_locked/2
       , dep_error/2
       , wdraw_created/2
       , wdraw_signed/2
       , wdraw_locked/2
       , wdraw_error/2
       , error/2
       , inband_msg/2
       , shutdown/2
       , shutdown_ack/2]).

-export([init/1
       , handle_call/3
       , handle_cast/2
       , handle_info/2
       , terminate/2
       , code_change/3]).

-record(st, {parent :: pid()
           , parent_mon_ref :: reference()
           , econn }).

channel_open       (Session, Msg) -> cast(Session, {msg, ?CH_OPEN      , Msg}).
channel_accept     (Session, Msg) -> cast(Session, {msg, ?CH_ACCEPT    , Msg}).
funding_created    (Session, Msg) -> cast(Session, {msg, ?FND_CREATED  , Msg}).
funding_signed     (Session, Msg) -> cast(Session, {msg, ?FND_SIGNED   , Msg}).
funding_locked     (Session, Msg) -> cast(Session, {msg, ?FND_LOCKED   , Msg}).
deposit_created    (Session, Msg) -> cast(Session, {msg, ?DEP_CREATED  , Msg}).
deposit_signed     (Session, Msg) -> cast(Session, {msg, ?DEP_SIGNED   , Msg}).
deposit_locked     (Session, Msg) -> cast(Session, {msg, ?DEP_LOCKED   , Msg}).
channel_reestablish(Session, Msg) -> cast(Session, {msg, ?CH_REESTABL  , Msg}).
update             (Session, Msg) -> cast(Session, {msg, ?UPDATE       , Msg}).
update_ack         (Session, Msg) -> cast(Session, {msg, ?UPDATE_ACK   , Msg}).
update_error       (Session, Msg) -> cast(Session, {msg, ?UPDATE_ERR   , Msg}).
dep_created        (Session, Msg) -> cast(Session, {msg, ?DEP_CREATED  , Msg}).
dep_signed         (Session, Msg) -> cast(Session, {msg, ?DEP_SIGNED   , Msg}).
dep_locked         (Session, Msg) -> cast(Session, {msg, ?DEP_LOCKED   , Msg}).
dep_error          (Session, Msg) -> cast(Session, {msg, ?DEP_ERR      , Msg}).
wdraw_created      (Session, Msg) -> cast(Session, {msg, ?WDRAW_CREATED, Msg}).
wdraw_signed       (Session, Msg) -> cast(Session, {msg, ?WDRAW_SIGNED , Msg}).
wdraw_locked       (Session, Msg) -> cast(Session, {msg, ?WDRAW_LOCKED , Msg}).
wdraw_error        (Session, Msg) -> cast(Session, {msg, ?WDRAW_ERR    , Msg}).
error              (Session, Msg) -> cast(Session, {msg, ?ERROR        , Msg}).
inband_msg         (Session, Msg) -> cast(Session, {msg, ?INBAND_MSG   , Msg}).
shutdown           (Session, Msg) -> cast(Session, {msg, ?SHUTDOWN     , Msg}).
shutdown_ack       (Session, Msg) -> cast(Session, {msg, ?SHUTDOWN_ACK , Msg}).

close(Session) ->
    try call(Session, close)
    catch
        error:_ -> ok
    end.

-define(GEN_SERVER_OPTS, []).

%% Connection establishment

connect(Host, Port, Opts) ->
    gen_server:start_link(
      ?MODULE, {self(), {connect, Host, Port, Opts}}, ?GEN_SERVER_OPTS).

accept(Port, Opts) ->
    gen_server:start_link(
      ?MODULE, {self(), {accept, Port, Opts}}, ?GEN_SERVER_OPTS).

init({Parent, Op}) ->
    proc_lib:init_ack(Parent, {ok, self()}),
    ParentMonRef = monitor(process, Parent),
    St = establish(Op, #st{parent = Parent,
                           parent_mon_ref = ParentMonRef}),
    gen_server:enter_loop(?MODULE, ?GEN_SERVER_OPTS, St).

establish({accept, Port, Opts}, St) ->
    TcpOpts = tcp_opts(listen, Opts),
    lager:debug("listen: TcpOpts = ~p", [TcpOpts]),
    {ok, LSock} = gen_tcp:listen(Port, TcpOpts),
    {ok, TcpSock} = gen_tcp:accept(LSock),
    %% TODO: extract/check something from FinalState?
    EnoiseOpts = enoise_opts(accept, Opts),
    lager:debug("EnoiseOpts (accept) = ~p", [EnoiseOpts]),
    {ok, EConn, _FinalSt} = enoise:accept(TcpSock, EnoiseOpts),
    %% tell_fsm({accept, EConn}, St),
    St#st{econn = EConn};
establish({connect, Host, Port, Opts}, St) ->
    TcpOpts = tcp_opts(connect, Opts),
    lager:debug("connect: TcpOpts = ~p", [TcpOpts]),
    {ok, TcpSock} = connect_tcp(Host, Port, TcpOpts),
    %% TODO: extract/check something from FinalState?
    EnoiseOpts = enoise_opts(connect, Opts),
    lager:debug("EnoiseOpts (connect) = ~p", [EnoiseOpts]),
    {ok, EConn, _FinalSt} = enoise:connect(TcpSock, EnoiseOpts),
    %% tell_fsm({accept, EConn}, St),
    St#st{econn = EConn}.

connect_tcp(Host, Port, Opts) ->
    {Timeout, Retries} = get_reconnect_params(),
    connect_tcp(Retries, Host, Port, Opts, Timeout).

connect_tcp(0, _, _, _, _) ->
    erlang:error(connect_timeout);
connect_tcp(Retries, Host, Port, Opts, Timeout) when Retries > 0 ->
    case gen_tcp:connect(Host, Port, Opts, Timeout) of
        {ok, _TcpSock} = Ok ->
            Ok;
        {error, _} ->
            timer:sleep(1000),
            connect_tcp(Retries-1, Host, Port, Opts, Timeout)
    end.

get_reconnect_params() ->
    %% {ConnectTimeout, Retries}
    {10000, 30}.


handle_call(close, _From, #st{econn = EConn} = St) ->
    close_econn(EConn),
    {stop, normal, ok, St};
handle_call(_Req, _From, St) ->
    {reply, {error, unknown_call}, St}.

handle_cast(Msg, St) ->
    try handle_cast_(Msg, St)
    catch
        error:Reason ->
            Trace = erlang:get_stacktrace(),
            lager:error("CAUGHT error:~p trace: ~p", [Reason, Trace]),
            erlang:error(Reason, Trace)
    end.

handle_cast_({msg, M, Info}, #st{econn = EConn} = St) ->
    enoise:send(EConn, aesc_codec:enc(M, Info)),
    {noreply, St};
handle_cast_(_Msg, St) ->
    {noreply, St}.

%% FSM had died
handle_info({'DOWN', Ref, process, Pid, _Reason},
            #st{parent_mon_ref=Ref, parent=Pid}=St) ->
    {stop, close, St};
handle_info(Msg, St) ->
    try handle_info_(Msg, St)
    catch
        error:Reason ->
            Trace = erlang:get_stacktrace(),
            lager:error("CAUGHT error:~p trace: ~p", [Reason, Trace]),
            erlang:error(Reason, Trace)
    end.

handle_info_({noise, EConn, Data}, #st{econn = EConn} = St) ->
    {_Type, _Info} = Msg = aesc_codec:dec(Data),
    tell_fsm(Msg, St),
    enoise:set_active(EConn, once),
    {noreply, St};
handle_info_(_Msg, St) ->
    {noreply, St}.

terminate(_Reason, #st{econn = EConn}) ->
    close_econn(EConn),
    ok.

code_change(_FromVsn, St, _Extra) ->
    {ok, St}.

close_econn(undefined) ->
    ok;
close_econn(EConn) ->
    enoise:close(EConn).


cast(P, Msg) ->
    lager:debug("to noise session ~p: ~p", [P, Msg]),
    gen_server:cast(P, Msg).

call(P, Msg) ->
    lager:debug("Call to noise session ~p: ~p", [P, Msg]),
    gen_server:call(P, Msg).

tell_fsm({_, _} = Msg, #st{parent = Parent}) ->
    aesc_fsm:message(Parent, Msg).

tcp_opts(_Op, Opts) ->
    case lists:keyfind(tcp, 1, Opts) of
        false -> tcp_defaults();
        {_, TcpOpts} ->
            [Opt || Opt <- tcp_defaults(),
                    not tcp_opt_member(Opt, TcpOpts)]
                ++ TcpOpts
    end.


noise_defaults() ->
    [{noise, <<"Noise_XK_25519_ChaChaPoly_BLAKE2b">>}].

tcp_defaults() ->
    [{active, true},
     {reuseaddr, true},
     {mode, binary}].

tcp_opt_member({mode,M}, L) ->
    %% handle supported short forms 'binary' and 'list'
    lists:keymember(mode, 1, L) orelse lists:member(M, L);
tcp_opt_member({K,_}, L) ->
    lists:keymember(K, 1, L).


enoise_opts(_Op, Opts0) ->
    Opts = lists:keydelete(tcp, 1, Opts0),
    [Opt || {K,_} = Opt <- noise_defaults(),
            not lists:keymember(K, 1, Opts)] ++ Opts.
