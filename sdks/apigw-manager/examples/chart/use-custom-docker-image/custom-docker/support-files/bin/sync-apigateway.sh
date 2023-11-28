#!/bin/bash

# 加载 apigw-manager 原始镜像中的通用函数
source /apigw-manager/bin/functions.sh

# 待同步网关名
gateway_name="bk-demo"

# 待同步网关、资源定义文件
definition_file="/data/definition.yaml"
resources_file="/data/resources.yaml"

title "begin to db migrate"
call_command migrate apigw

title "syncing apigateway"
must_call_definition_command sync_apigw_config "${definition_file}" --gateway-name=${gateway_name}
must_call_definition_command sync_apigw_stage "${definition_file}" --gateway-name=${gateway_name}
must_call_definition_command sync_apigw_resources "${resources_file}" --gateway-name=${gateway_name} --delete
must_call_definition_command sync_resource_docs_by_archive "${definition_file}" --gateway-name=${gateway_name} --safe-mode
must_call_definition_command grant_apigw_permissions "${definition_file}" --gateway-name=${gateway_name}

title "fetch apigateway public key"
apigw-manager.sh fetch_apigw_public_key --gateway-name=${gateway_name} --print > "apigateway.pub"

title "releasing"
must_call_definition_command create_version_and_release_apigw "${definition_file}" --gateway-name=${gateway_name}

title "done"
