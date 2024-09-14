import json
import os
import re
import time
from copy import copy

import requests

from huhk.case_project.project_init import ProjectInIt
from huhk.unit_dict import Dict


class ProjectString(ProjectInIt):
    def _get_description(self, req_body_other):
        try:
            if not req_body_other:
                return []
            elif isinstance(req_body_other, str):
                try:
                    properties = json.loads(req_body_other).get('properties') or {}
                except:
                    properties = {}
            elif isinstance(req_body_other, list):
                return req_body_other
            else:
                try:
                    properties = req_body_other.get('properties') if req_body_other.get('properties') else req_body_other
                except:
                    properties = {}
            _list = []
            for k, v in properties.items():
                if type(v) == dict:
                    _properties = self._get_description(v.get('properties')) if v.get('properties') else None
                    _items = self._get_description(v.get('items')) if v.get('items') else None
                    _row = {"name": k,
                            "desc": v.get('description', ""),
                            "type": v.get('type', ""),
                            "properties": _properties,
                            "items": _items}
                else:
                    _row = {"name": k,
                            "desc": None,
                            "type": v,
                            "properties": None,
                            "items": None}
                _list.append(_row)
            return _list
        except Exception as e:
            print(e)

    @staticmethod
    def get_service_fun_value():
        """
            生成所有项目公共方法文件
        """
        value = "import requests\n\nfrom huhk.unit_fun import FunBase\nfrom huhk.unit_redis import Redis\n"
        value += "from huhk.unit_dict import Dict\nfrom huhk.unit_logger import logger\n"
        value += f"from huhk import admin_host\n\n\nclass ServiceFun(FunBase):\n"
        value += "    def __init__(self):\n        super().__init__()\n        self.res = None\n"
        value += "        self.output_list = Dict()\n        self.input_value = Dict()\n\n"
        value += """    @staticmethod
    def run_mysql(sql_str, db_id=1, db_name=None):
        sql_str_l = re.split(r'\swhere\s', sql_str, 1, re.I)
        if db_name and isinstance(db_name, str):
            db_name = db_name.strip()
            sql_str_l_0 = re.split(r'\sfrom\s', sql_str_l[0], 1, re.I)
            for i in [i.strip().split()[0] for i in re.split(r'\sjoin\s', sql_str_l_0[1].strip(), 100, re.I)]:
                sql_str_l_0[1] = sql_str_l_0[1].replace(i, f"{db_name}.{i}")
                sql_str_l_0[1] = sql_str_l_0[1].replace(f"{db_name}.{db_name}.", f"{db_name}.")
            sql_str_l[0] = " from ".join(sql_str_l_0)
        sql_str_l[-1] = sql_str_l[-1].replace('[', '(').replace(']', ')')
        sql_str = " where ".join(sql_str_l)

        logger.info("执行sql：" + sql_str)
        out = requests.post(admin_host + "/sql/running_sql/", json={"id": db_id, "sql_str": sql_str}).json()
        logger.info("sql执行结果：" + str(out))
        if out.get("code") == "0000":
            return [Dict(i) for i in out.get("data")] if out.get("data") and isinstance(out.get("data"), list) and isinstance(out.get("data")[0], dict) else out.get("data")
        else:
            assert False, sql_str + str(out.get("msg"))\n\n"""
        value += """    @staticmethod
    def get_redis(key=""):
        r = Redis(host="r-bp1tnpcfs5gtqr7s8kpd.redis.rds.aliyuncs.com", port=6379, password="Geelypk2022", db=1)
        out = r.get(key)
        try:
            out = eval(out)
        except:
            pass
        return out\n\n"""
        value += f"if __name__ == '__main__':\n    f = ServiceFun()\n"
        value += '    out = f.faker2.name()\n    print(out)\n\n'
        return value

    def get_init_value(self):
        """
            生成项目__init__.py文件
        """
        value = 'from huhk.init_project import GetApi\n'
        value += 'from service import Request\n\n'
        value += f'APP_KEY = "{self.app_key}"\n\n\n' if self.app_key else ""
        value += 'unit_request = Request("SIT", APP_KEY)\n'
        value += '# 环境变量\nvariable = unit_request.variable\n'
        value += 'http_requester = unit_request.http_requester\n\n\n'
        value += 'if __name__ == "__main__":\n'
        value += f"    GetApi(name='{self.name}'"
        if self.app_key:
            value += f", app_key=APP_KEY"
        elif self.yapi_url and self.yapi_token:
            value += f", yapi_url='{self.yapi_url}', yapi_token='{self.yapi_token}'"
        elif self.yapi_json_file:
            value += f", yapi_json_file='{self.yapi_json_file}'"
        elif self.swagger_url:
            value += f", swagger_url='{self.swagger_url}'"
        value += ").create_or_update_project()\n"
        return value

    def get_add_api_value(self):
        value = "from huhk.case_project.main_fun import fun_project\n\n" \
                f"fun_project(name=\"{self.name}\")\n"
        return value

    def get_fun_value(self):
        """生成项目基础方法"""
        value = "from service.service_fun import ServiceFun\n\n"
        value += f"class {self.name2}Fun(ServiceFun):\n"
        value += "    @staticmethod\n    def run_mysql(sql_str, db_id=1, db_name=None):\n"
        value += '        return ServiceFun.run_mysql(sql_str, db_id, db_name)\n\n\n'
        value += f"if __name__ == '__main__':\n    f = {self.name2}Fun()\n"
        value += '    out = f.faker2.name()\n'
        value += '    print(out)\n\n'
        return value

    def get_conftest_value(self):
        """生成标签文件"""
        value = ("import pytest\n\n\ndef pytest_configure(config):\n"
                 '    config.addinivalue_line("markers", "smoke:冒烟用例")\n'
                 '    config.addinivalue_line("markers", "success:正向用例")\n'
                 '    config.addinivalue_line("markers", "failed:逆向用例")\n'
                 '    config.addinivalue_line("markers", "get:查询用例")\n'
                 '    config.addinivalue_line("markers", "fun:功能用例")\n\n')

        return value

    @staticmethod
    def get_params_string(req_all, res_body):
        """方法描述生成"""
        def get_str(l):
            _str = ""
            if l:
                for p in l:
                    _str += f'    params: {p.get("name", "")} : {p.get("type", "")} : {p.get("desc", "")}\n'
                    if p.get('properties') or p.get('items'):
                        for p2 in p.get('properties') or p.get('items'):
                            _str += f'              {p2.get("name", "")} : {p2.get("type", "")} : {p2.get("desc", "")}\n'
            return _str

        try:
            api_str = get_str(req_all)
            api_str += "    params: headers : 请求头\n    ====================返回======================\n"
            api_str += get_str(res_body)
            return api_str
        except Exception as e:
            print(e)

    @staticmethod
    def list_add(_list):
        """列表变量叠加"""
        _list3 = []
        _list4 = ["Content-Type"]
        for i in _list:
            name = i.get("name").split("[")[0].split(".")[0]
            for name in name.split("|"):
                if name.strip() not in _list4:
                    _list4.append(name.strip())
                    j = copy(i)
                    j["name"] = name.strip()
                    _list3.append(j)
        return _list3

    @staticmethod
    def get_req_json(_list, value=False):
        """"""
        json_str = '{\n'
        for p in _list:
            if p.get("name") not in ('authorization', ):
                json_str += f'        "{p.get("name", "")}": ' + (
                    '"%s"' % p.get("value", "") if value else p.get("name", "")) + ","
                json_str += ("  # " + p.get("desc").replace('\n', ' ') if p.get("desc") else "") + '\n'
        json_str += '    }'
        return json_str

    @staticmethod
    def get_fun_name(name):
        name_l = name.split('/')
        for i, v in enumerate(name_l):
            if v.isdigit():
                name_l[i] = "{id}"
        name = '/'.join(name_l)
        name = re.sub(r'\W', '_', name.split('{')[0]).strip().lstrip('_').lower()
        return name

    def get_path(self, name, fun_type="apis"):
        name_l = [(i if i != "import" else i + "1") for i in name.split('_') if i]
        out = Dict()
        if fun_type == "apis" and self.this_fun_list.api.get(name):
            filename = self.this_fun_list.api[name].path
            out.path = filename
            out.class_name = None
            out.import_path = ".".join(filename.replace(self.path.dir, "").split(os.sep)[1:])[:-3]
        elif fun_type == "test":
            filename = f"test_{name}.py".replace('__', "_")
            out.path = os.path.join(self.path.testcase_dir, os.path.sep.join(name_l[:-1]), filename)
            out.class_name = filename.split(".")[0].title().replace('_', '')
            out.import_path = None
        else:
            filename = f"{fun_type}_{'_'.join(name_l[:-1]) if name_l[:-1] else self.name}.py".replace('__', "_")
            out.path = os.path.join(self.path.service_dir, fun_type, os.path.sep.join(name_l[:-2]), filename)
            out.class_name = filename.split(".")[0].title().replace('_', '')
            out.import_path = ".".join(["service", self.name, fun_type] + name_l[:-2] + [filename.split('.py')[0]])
        return out

    def get_api_header_str(self, import_path):
        api_header_str = f"import allure\n\nfrom service.{self.name} import http_requester\n" \
                         f"from huhk.unit_request import UnitRequest\n" \
                         f"from {import_path.rsplit('.', 1)[0]} import _route as route\n" \
                         f"from {import_path.rsplit('.', 1)[0]} import _host as host\n" \
                         f"from {import_path.rsplit('.', 1)[0]} import _token as token\n\n" \
                         f"_route = \"\" or route\n" \
                         f"_host = \"\" or host\n" \
                         f"_token = \"\" or token\n\n\n"
        return api_header_str

    @staticmethod
    def get_api_header_str2(import_path, api_str):
        host_str = f"from {import_path.rsplit('.', 1)[0]} import _host as host\n"
        token_str = f"from {import_path.rsplit('.', 1)[0]} import _token as token\n"
        if token_str not in api_str:
            api_str = api_str.replace(host_str, host_str + token_str, 1)
            api_str = api_str.replace(" or host\n", " or host\n_token = \"\" or token\n", 1)
        return api_str

    def get_api_init_str(self, import_path):
        if import_path.count('.') > 1:
            api_str = f"from {import_path} import _route as route\n" \
                      f"from {import_path} import _host as host\n" \
                      f"from {import_path} import _token as token\n\n" \
                      f"_route = \"\" or route\n" \
                      f"_host = \"\" or host\n" \
                      f"_token = \"\" or token\n\n"
        else:
            api_str = f"_route = \"{self.base_path}\"\n" \
                      f"_host = \"HOST\"\n" \
                      f"_token = \"TOKEN\"\n"
        return api_str

    @staticmethod
    def get_api_init_str2(init_str, import_path):
        if import_path.count('.') > 1:
            token_str = f"from {import_path} import _token as token\n"
            if token_str not in init_str:
                host_str = f"from {import_path} import _host as host\n"
                init_str = init_str.replace(host_str, host_str + token_str, 1)
                init_str = init_str.replace(" or host\n", " or host\n_token = \"\" or token\n", 1)
        else:
            if "_token =" not in init_str:
                init_str += f"\n_token = \"TOKEN\"\n"
                init_str = init_str.replace("\n\n_token", "\n_token")
        return init_str

    def get_api_fun_str(self, name, row, type=1):
        """type: 1：根据接口文档自动生成， 2：自主更新，3：自主添加，4：增量覆盖"""
        if type == 1:
            if self.yapi_url and self.yapi_token:
                data = {"token": self.yapi_token, "id": row.get('_id')}
                res = requests.get(self.yapi_url + "/api/interface/get", data=data)
                if res:
                    res = Dict(json.loads(res.text)).get('data')
                    res.update(row)
                    row = res
        api_str = '@allure.step(title="调接口：%s")\n' % row.get("path").split('{')[0]
        api_str += "def " + name + "("
        if type == 1:
            req_params = row.get('req_params', [])
            req_query = row.get('req_query', [])
            req_body_form = row.get('req_body_form', [])
            req_headers = row.get('req_headers', [])
            req_body = self._get_description(row.get('req_body_other'))
            res_body = self._get_description(row.get('res_body'))
            req_all = self.list_add(req_params + req_query + req_body_form + req_body)
            req_all_data = self.list_add(req_query + req_body_form + req_body)

        elif type == 2:
            try:
                try:
                    data = json.loads(row.data)
                except:
                    data = eval(row.data)
            except:
                data = re.split(r'&', row.data)
                data = {i.split("=")[0]: i.split("=")[1] for i in data if "=" in i}
            req_headers = [Dict({"name": k, "value": v}) for k, v in row.headers.items()]
            data = {str(k).strip(): v for k, v in data.items()}
            req_all = [Dict({"name": k, "value": v}) for k, v in data.items()]
            res_body = []
            if row.method == "GET":
                req_all_data = []
                req_params = req_all
            else:
                req_all_data = req_all
                req_params = []
            row.tag = row.name.split(":")[0] if ":" in row.name else ""
            row.title = row.name.split(":")[-1]
        if "{" in row.get("path"):
            tmp = re.findall(r'{(.+?)}', row.get("path"))
            if tmp:
                for tmp1 in tmp:
                    if f"'{tmp1}'" not in str(req_all):
                        req_all += [Dict({"name": tmp1, "value": None})]
        api_str += f"{' '.join(set([i['name'] + '=None,' for i in req_all]))} headers=None, **kwargs):".strip()
        api_str += f'\n    """\n    {"".join(row.get("tag") or [])}: {row.get("title")}\n' \
                   f'    up_time={int(time.time())}\n\n'
        api_str += self.get_params_string(req_all, res_body)
        api_str += f'    """\n    _method = "{row.get("method")}"\n    _url = "{row.get("path")}"\n'
        if '/{' in row.get("path"):
            api_str += f'    _url = UnitRequest.get_url(_url, locals())\n'
        api_str += '    kwargs["_route"] = kwargs.get("_route", _route)\n'
        api_str += '    kwargs["_host"] = kwargs.get("_host", _host)\n'
        api_str += '    kwargs["_token"] = kwargs.get("_token", _token)\n'
        api_str += '\n    _headers = ' + self.get_req_json(req_headers, True)
        api_str += '\n    _headers.update({"headers": headers})\n\n'
        api_str += '    _data = ' + self.get_req_json(req_all_data)
        api_str += '\n\n    _params = ' + self.get_req_json(req_params)

        api_str += '\n\n    return http_requester(_method, _url, params=_params, data=_data, ' \
                   'headers=_headers, **kwargs)\n\n'
        return api_str.replace("( ", "(")

    def get_api_fun_str2(self, ord_str, name, row, type=1):
        """type: 1：根据接口文档自动生成， 2：自主更新，3：自主添加，4：增量覆盖"""
        if type == 1:
            if self.yapi_url and self.yapi_token:
                data = {"token": self.yapi_token, "id": row.get('_id')}
                res = requests.get(self.yapi_url + "/api/interface/get", data=data)
                if res:
                    res = Dict(json.loads(res.text)).get('data')
                    res.update(row)
                    row = res

            req_params = row.get('req_params', [])
            req_query = row.get('req_query', [])
            req_body_form = row.get('req_body_form', [])
            req_body = self._get_description(row.get('req_body_other'))
            req_all = self.list_add(req_params + req_query + req_body_form + req_body)
            req_all_data = self.list_add(req_query + req_body_form + req_body)

        elif type == 2:
            try:
                data = json.loads(row.data)
            except:
                try:
                    data = eval(row.data)
                except:
                    if re.findall("\{[\d\D]+\}", row.data.strip()):
                        data = {i: None for i in re.findall("[\"\'](.+?)[\"\'] *:", row.data.strip())}
                    else:
                        data = {i.split("=")[0]: i.split("=")[1] for i in re.split(r'&', row.data) if "=" in i}

            req_all = [Dict({"name": k.strip(), "value": v}) for k, v in data.items()]
            if row.method == "GET":
                req_all_data = []
                req_params = req_all
            else:
                req_all_data = req_all
                req_params = []
            row.tag = row.name.split(":")[0] if ":" in row.name else ""
            row.title = row.name.split(":")[-1]

        for i in req_all:
            if i['name'].strip() + '=None' not in ord_str and i['name'] not in ('authorization', ):
                ord_str = ord_str.replace("headers=None,", i['name'] + '=None, headers=None,', 1)

        for i in req_all_data:
            desc = (i.get("desc", "") or "").replace("\n", " ")
            if f'"{i.get("name").strip()}": {i.get("name").strip()},' not in ord_str and i['name'] not in ('authorization', ):
                tmp_str = f'        "{i.get("name", "").strip()}": {i.get("name", "").strip()},  # {desc}\n'
                ord_str = ord_str.replace("    _data = {\n", "    _data = {\n" + tmp_str, 1)
        for i in req_params:
            desc = (i.get("desc", "") or "").replace("\n", " ")
            if f'"{i.get("name").strip()}": {i.get("name").strip()},' not in ord_str and i['name'] not in ('authorization',):
                tmp_str = f'        "{i.get("name", "").strip()}": {i.get("name", "").strip()},  # {desc}\n'
                ord_str = ord_str.replace("    _params = {\n", "    _params = {\n" + tmp_str, 1)

        if '    kwargs["_token"] = kwargs.get("_token", _token)\n' not in ord_str:
            ord_str = ord_str.replace(' _host)\n', ' _host)\n    kwargs["_token"] = kwargs.get("_token", _token)\n', 1)

        return ord_str

    def get_sql_header_str(self, class_name):
        header_str = f"from service.{self.name}.{self.name}_fun import {self.name2}Fun\n\n\n"
        header_str += f"class {class_name}({self.name2}Fun):\n"
        return header_str

    @staticmethod
    def get_sql_fun_str(fun_name):
        sql_fun_str = "    def sql_%s(self, **kwargs):\n" % fun_name
        sql_fun_str += "        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段\n"
        sql_fun_str += "        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  "
        sql_fun_str += "# 模糊查询字段，数组包含查询字段，区间字段处理\n"
        sql_fun_str += '        # kwargs["order_by"] = None  # 排序\n'
        sql_fun_str += '        sql_str = self.get_sql_str("table_name", **kwargs)  # 生成sql语句\n'
        sql_fun_str += '        # out = self.run_mysql(sql_str)  # 执行sql语句\n' \
                       '        # return out\n\n'
        return sql_fun_str

    def get_teardown_header_str(self, class_name):
        header_str = f"import allure\n\n"
        header_str += f"from service.{self.name}.{self.name}_fun import {self.name2}Fun\n\n\n"
        header_str += f"class {class_name}({self.name2}Fun):\n"
        return header_str

    @staticmethod
    def get_teardown_fun_str(fun_name):
        teardown_fun_str = f'    @allure.step(title="测试数据恢复")\n'
        teardown_fun_str += "    def teardown_%s(self, **kwargs):\n" % fun_name
        teardown_fun_str += '        sql_str = f"delete from table where name=\'{self.input_value.%s.name}\'"\n' % fun_name
        teardown_fun_str += '        # out = self.run_mysql(sql_str)  # 执行sql语句\n'
        teardown_fun_str += '        # return out\n\n'
        return teardown_fun_str

    def get_assert_header_str(self, class_name, sql_path, teardown_path):
        header_str = f"import allure\n\n"
        header_str += f"from service.{self.name} import unit_request\n"
        header_str += f"from {sql_path.import_path} import {sql_path.class_name}\n"
        header_str += f"from {teardown_path.import_path} import {teardown_path.class_name}\n\n\n"
        header_str += f"class {class_name}({sql_path.class_name}, {teardown_path.class_name}):\n"
        return header_str

    @staticmethod
    def get_assert_header_str2(file_str, sql_path, teardown_path):
        if f"from {teardown_path.import_path} import {teardown_path.class_name}\n" not in file_str:
            file_str = file_str.replace(f"import {sql_path.class_name}\n",
                                        f"import {sql_path.class_name}\nfrom {teardown_path.import_path} import {teardown_path.class_name}\n", 1)
            file_str = file_str.replace(f"({sql_path.class_name})", f"({sql_path.class_name}, {teardown_path.class_name})")
        return file_str

    def get_assert_fun_str(self, fun_name):
        assert_fun_str = f'    @allure.step(title="接口返回结果校验")\n' \
                         f'    def assert_{fun_name}(self, _assert=True, **kwargs):\n' \
                         f'        flag, msg = unit_request.is_assert_code_true(self.res, _assert)\n' \
                         f'        with allure.step("校验接口返回code"):\n' \
                         f'            assert flag, "校验接口返回code失败，" + msg\n' \
                         f'        if _assert is True and flag:\n' \
                         f'            with allure.step("接口返回数据格式校验"):\n' \
                         f'                flag, msg = unit_request.is_assert_compare_status(self.res)\n' \
                         f'                assert flag, "接口数据格式校验失败，" + msg\n' \
                         f'        # if _assert is True and flag:\n' \
                         f'        #     with allure.step("业务校验"):\n' \
                         f'        #         out = self.sql_{fun_name}(**kwargs)\n'
        assert_fun_str += '        #         flag = self.compare_json_list(self.res, out, [%s])\n' % \
                          ', '.join(['"%s"' % i for i in self.this_fun_list.api[fun_name].input
                                     if str(i).lower() not in self.page_and_size])
        assert_fun_str += '        #         assert flag, "数据比较不一致"\n\n'
        return assert_fun_str

    def get_api_fun_header_str(self, fun_name):
        assert_path = self.get_path(fun_name, fun_type='asserts')
        fun_path = self.get_path(fun_name, fun_type='funs')
        api_path = self.get_path(fun_name, fun_type='apis')
        header_str = "import allure\n\n"
        header_str += f"from {assert_path.import_path} import {assert_path.class_name}\n"
        header_str += f"from {api_path.import_path.rsplit('.', 1)[0]} import {api_path.import_path.rsplit('.', 1)[1]}\n\n\n"
        header_str += f"class {fun_path.class_name}({assert_path.class_name}):\n"
        return header_str

    def get_api_fun_header_str2(self, fun_name, file_str):
        assert_path = self.get_path(fun_name, fun_type='asserts')
        api_path = self.get_path(fun_name, fun_type='apis')
        header_str = "import allure\n"
        if header_str not in file_str:
            file_str = header_str + file_str
        header_str = f"from {assert_path.import_path} import {assert_path.class_name}\n"
        if header_str not in file_str:
            file_str = header_str + file_str
            file_str = file_str.replace("):", f", {assert_path.class_name}):", 1)
        header_str = f"from {api_path.import_path.rsplit('.', 1)[0]} import {api_path.import_path.rsplit('.', 1)[1]}\n"
        if header_str not in file_str:
            file_str = header_str + file_str
        return file_str

    def get_api_fun_fun_str(self, fun_name):
        api_path = self.get_path(fun_name, fun_type='apis')
        api = self.this_fun_list.api[fun_name]
        data_list_tmp = []
        for n in api.input:
            if n in self.size_names:
                data_list_tmp.append(n.strip() + '=10')
            elif n in self.page_names:
                data_list_tmp.append(n.strip() + '=1')
            else:
                data_list_tmp.append(n.strip() + '="$None$"')
        api_fun_fun_str = f"    @allure.step(title=\"{api.title or api.url}\")\n"
        api_fun_fun_str += "    def %s(self, %s, _assert=True, " % (fun_name, ", ".join(data_list_tmp))
        data_list = [n for n in api.input if n not in self.page_and_size and n != 'headers']
        if str(api.method).lower() == "post" and not (set(api.input) & set(self.page_and_size)) and len(api.input) > 1:
            api_fun_fun_str += "_all_is_None=False, "
        api_fun_fun_str += " **kwargs):\n"
        api_fun_fun_str += f"        \"\"\"\n            url={api.url}\n"
        api_fun_fun_str += "".join([" " * 16 + i.strip() + "\n" for i in api.params.split('\n')
                                    if i.strip() and "params: userId" not in i])
        api_fun_fun_str += "        \"\"\"\n"
        if set(api.input) & set(self.page_and_size) or (str(api.method).lower() == "get" and len(data_list) > 1):
            api_fun_fun_str += "        _key = \".\"\n"
            for n in data_list:
                api_fun_fun_str += f"        {n} = self.get_list_choice({n}, list_or_dict=None, key=_key)\n"
        else:
            api_fun_fun_str += "        _key = \"\"\n"
            for n in data_list:
                if len(data_list) > 1:
                    api_fun_fun_str += f"        {n} = self.get_value_choice({n}, list_or_dict=None, key=_key," \
                                       f" _all_is_None=_all_is_None)\n"
                else:
                    api_fun_fun_str += "        %s = self.get_value_choice(%s, list_or_dict=None, key=_key)\n" % (n, n)
        api_fun_fun_str += '\n' if data_list else ''
        api_fun_fun_str += "        _kwargs = self.get_kwargs(locals())\n"
        api_fun_fun_str += f"        self.res = {api_path.import_path.rsplit('.', 1)[1]}.{fun_name}(**_kwargs)\n\n"
        api_fun_fun_str += "        self.assert_%s(_assert, **_kwargs)\n" % fun_name
        api_fun_fun_str += "        self.set_output_value(_kwargs)\n"
        api_fun_fun_str += "        self.set_value(_kwargs)\n\n\n"
        api_fun_fun_str = api_fun_fun_str.replace(", , ", ", ")
        return api_fun_fun_str

    def get_api_fun_fun_str2(self, ord_str, fun_name):
        api = self.this_fun_list.api[fun_name]
        ord_input = re.findall(r"def .+?\((.*)\)", ord_str)[0].split(",")
        ord_input = [i.strip().split("=")[0] for i in ord_input if "=" in i]
        data_list = set(api.input) - set(ord_input)
        if data_list:
            data_list_tmp = []
            for n in data_list:
                if n in self.size_names:
                    data_list_tmp.append(n.strip() + '=10')
                elif n in self.page_names:
                    data_list_tmp.append(n.strip() + '=1')
                else:
                    data_list_tmp.append(n.strip() + '="$None$"')
            ord_str = ord_str.replace("(self,", f"(self, {', '.join(data_list_tmp)},", 1)

            if str(api.method).lower() == "post" and not (set(api.input) & set(self.page_and_size)) and len(api.input) > 1:
                if "_all_is_None=False, " not in ord_str:
                    ord_str = ord_str.replace("**kwargs):", "_all_is_None=False, **kwargs):", 1)

            if set(api.input) & set(self.page_and_size) or (str(api.method).lower() == "get" and len(data_list) > 1):
                if "        _key =" not in ord_str:
                    ord_str = ord_str.replace("\n        _kwargs ", "\n        _key = \".\"\n        _kwargs ")
                for n in data_list:
                    _str = f"\n        {n} = self.get_list_choice({n}, list_or_dict=None, key=_key)"
                    ord_str = ord_str.replace("\n        _kwargs ", _str + "\n        _kwargs ")
            else:
                if "        _key =" not in ord_str:
                    ord_str = ord_str.replace("\n        _kwargs ", "\n        _key = \"\"\n        _kwargs ")
                for n in data_list:
                    if "_all_is_None" in ord_str:
                        _str = f"\n        {n} = self.get_value_choice({n}, list_or_dict=None, key=_key, " \
                               f"_all_is_None=_all_is_None)"
                    else:
                        _str = f"\n        {n} = self.get_value_choice({n}, list_or_dict=None, key=_key)"
                    ord_str = ord_str.replace("\n        _kwargs ", _str + "\n        _kwargs ")
        return ord_str

    def get_api_testcase_header_str(self, fun_name):
        api = self.this_fun_list.api[fun_name]
        header_str = "import allure\nimport pytest\n\n"
        header_str += f"from service.{self.name}.funs.funs_{self.name} " \
                      f"import Funs{self.name.title().replace('_', '')}\n\n\n"
        header_str += f"@allure.epic(\"服务模块:{self.name3 or ''}\")\n"
        header_str += f"@allure.feature(\"二级模块:" \
                      f"{api.title.strip().split(':')[0].strip() if ':' in api.title else ''}\")\n"
        header_str += f"@allure.story(\"接口名称：" \
                      f"{api.title.strip().split(':', 1)[1].strip() if ':' in api.title else api.title.strip()}" \
                      f"，接口（{api.url}）\")\n"
        header_str += f"class Test{fun_name.title().replace('_', '')}:\n"
        header_str += f"    def setup(self):\n"
        header_str += f"        self.f = Funs{self.name.title().replace('_', '')}()\n\n"
        header_str += f"    def teardown(self):\n"
        header_str += f"        self.f.teardown_%s()\n\n" % fun_name
        return header_str

    @staticmethod
    def get_api_testcase_header_str2(file_str, fun_name):
        if f"def teardown(self):" not in file_str:
            file_str = file_str.replace("    @Funs", f"\n    def teardown(self):\n"
                                                     f"        self.f.teardown_{fun_name}()\n\n    @Funs", 1)
        return file_str

    def get_api_testcase_str(self, fun_name):
        api = self.this_fun_list.api[fun_name]
        out = Dict()
        data_list = [n for n in api.input if n not in self.page_and_size and n != 'headers']

        def get_str(n1="", n2="", n3="", severity="3", is_smoke=False, is_success=True, is_get=True):
            name = f"{fun_name}{'__' + n2 if n2 else ''}"
            _str = f'    @Funs{self.name2}.title_severity_mark(' \
                   f'"{api.title or api.url}{"__" + n1 if n1 else ""}", "#skip", ' \
                   f'"{severity}", ' \
                   f'"{"smoke" if is_smoke else "#smoke"}", ' \
                   f'"{"success" if is_success else "#success"}", ' \
                   f'"{"failed" if not is_success else "#failed"}", ' \
                   f'"{"get" if is_get else "#get"}", ' \
                   f'"{"fun" if not is_get else "#fun"}")\n'
            _str += f"    def test_{fun_name}{'__' + n2 if n2 else ''}(self):\n"
            _str += f"        self.f.{fun_name}({n3})\n\n"
            return name, _str

        name, fun_str = get_str("", "", "", severity="2", is_smoke=True)
        out[name] = fun_str
        if data_list:
            if set(api.input) & set(self.page_and_size) or (str(api.method).lower() == "get" and len(data_list) > 1):
                if set(api.input) & set(self.page_names):
                    name, fun_str = get_str(f"翻页", list(set(api.input) & set(self.page_names))[0],
                                            ", ".join([f"{n}=2" for n in (set(api.input) & set(self.page_names))]))
                    out[name] = fun_str
                if set(api.input) & set(self.size_names):
                    name, fun_str = get_str(f"每页条数", list(set(api.input) & set(self.size_names))[0],
                                            ", ".join([f"{n}=20" for n in (set(api.input) & set(self.size_names))]))
                    out[name] = fun_str
                for n in data_list:
                    name, fun_str = get_str(f"单参数有值： {n}", n, f"{n}=True")
                    out[name] = fun_str
                if len(data_list) > 1:
                    name, fun_str = get_str(f"所有参数有值", "all", ", ".join([f"{n}=True" for n in data_list]))
                    out[name] = fun_str
            else:
                for n in data_list:
                    name, fun_str = get_str(f"入参 {n} 为空", n, f"{n}=None", is_get=False)
                    out[name] = fun_str
                if len(data_list) > 1:
                    name, fun_str = get_str(f"所有入参都为空", "null", f"_all_is_None=True", is_get=False)
                    out[name] = fun_str
        return out

