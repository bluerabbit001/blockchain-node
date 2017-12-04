%%% -*- erlang-indent-level: 4 -*-
%%%-------------------------------------------------------------------
%%% @copyright (C) 2017, Aeternity Anstalt
%%%-------------------------------------------------------------------

-type(option()  :: {atom(), any()}).
-type(options() :: [option()]).


-type workers() :: orddict:orddict(pid(), atom()).
-type mining_state() :: 'running' | 'stopped'.

-record(candidate, {block     :: block(),
                    nonce     :: aec_pow:nonce(),
                    max_nonce :: aec_pow:nonce(),
                    top_hash  :: binary()
                   }).


-record(state, {block_candidate                   :: #candidate{} | 'undefined',
                blocked_tags            = []      :: ordsets:ordsets(atom()),
                chain_state                       :: aec_chain_state:state(),
                fetch_new_txs_from_pool = true    :: boolean(),
                keys_ready              = false   :: boolean(),
                mining_state            = running :: mining_state(),
                seen_top_block_hash               :: binary() | 'undefined',
                workers                 = []      :: workers()
               }).
