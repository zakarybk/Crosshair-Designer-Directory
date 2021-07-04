import re
import json
import requests

CROSS_CONFIGS_SOURCE = 'https://raw.githubusercontent.com/zakarybk/crosshair_designer/master/lua/crosshair-designer/load.lua'


def _remove_lua_c_comments(text):
    text = re.sub(re.compile("/\*.*?\*/", re.DOTALL),
                  "", text)  # (/*COMMENT */)
    text = re.sub(re.compile("//.*?\n"), "", text)  # (//COMMENT\n )
    text = re.sub(re.compile("--.*?\n"), "", text)  # (--COMMENT\n )
    return text


def _json_loads_from_crosshair_load(load_data_file):
    tbl_start = load_data_file.find('CrosshairDesigner.SetUpConvars({')
    tbl_end = load_data_file.find('})', tbl_start)

    # Just the crosshair config Lua table from the codebase
    tbl_start_next_line = tbl_start + \
        load_data_file[tbl_start:tbl_end].find('\n') + len('\n')
    tbl_end_prev_line = tbl_end  # ignore white space later

    # JSON [] tags
    tbl = '[' + load_data_file[tbl_start_next_line:tbl_end_prev_line] + ']'
    # JSON var assignment
    tbl = tbl.replace('=', ':')

    # JSON keys:values wrapped in ""
    tbl = re.sub('([a-zA-Z0-9]+):', r'"\1":', tbl)
    tbl = re.sub(':([-?a-zA-Z0-9]+)', r':"\1"', tbl)

    # Remove conflicting syntax instead of fixing it
    tbl = re.sub(re.compile("\"help\".*?\n"), '', tbl)
    tbl = re.sub(re.compile("\"title\".*?\n"), '', tbl)

    # Remove trailing commas (invalid JSON - not Lua)
    tbl = re.sub(re.compile('\,(?=\s*?[\}\]])'), '', tbl)

    return json.loads(_remove_lua_c_comments(tbl))


def crosshair_configs():
    req = requests.get(CROSS_CONFIGS_SOURCE)
    configs = _json_loads_from_crosshair_load(req.text)
    return configs
