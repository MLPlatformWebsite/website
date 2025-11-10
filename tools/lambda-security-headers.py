""" Ensure that the security headers Lambda is connected to the CF Distribution """
#!/usr/bin/python3


import sys
import os
import boto3


_CFDIST = (
    "CF_DIST_ID_STATIC_LO"
)
_LAMBDA_ARN = (
    "CLOUDFRONT_ADD_SECURITY_HEADERS_ARN"
)
_LAMBDA_FUNC = (
    "CLOUDFRONT_SECURITY_HEADERS_FUNC"
)


def get_env_var(env):
    """ Return the value for the required environment variable or exit with error """
    env_value = os.environ.get(env)
    if env_value is None:
        sys.exit("Cannot retrieve environment variable '%s'" % env)
    return env_value


def build_lambda_arn(function_name) -> str:
    """ Get the latest version for the function """
    session = boto3.Session()
    client = session.client('lambda', 'us-east-1')
    versions = client.list_versions_by_function(FunctionName=function_name)["Versions"]
    # Find the highest version number
    highest_ver = None
    highest_arn = None
    for version in versions:
        if version["Version"] != "$LATEST":
            ver = int(version["Version"])
            if highest_ver is None or ver > highest_ver:
                highest_ver = ver
                highest_arn = version["FunctionArn"]
    if highest_arn is None:
        sys.exit(f"Unable to find function {function_name}")
    return highest_arn


def get_lambda_arn() -> str:
    """ Return the ARN for the Lambda function """
    function_name = os.environ.get(_LAMBDA_FUNC)
    if function_name is not None:
        return build_lambda_arn(function_name)

    return get_env_var(_LAMBDA_ARN)


def is_function_attached():
    """ Is the function attached to the distribution? """
    func = get_lambda_arn()
    session = boto3.Session()
    cf_client = session.client('cloudfront', 'us-east-1')
    config = cf_client.get_distribution_config(
        Id=get_env_var(_CFDIST)
    )
    distrib_config = config["DistributionConfig"]
    dcb = distrib_config["DefaultCacheBehavior"]
    if ("LambdaFunctionAssociations" not in dcb or
            "Items" not in dcb["LambdaFunctionAssociations"]):
        return False
    for lfa in dcb["LambdaFunctionAssociations"]["Items"]:
        if lfa["LambdaFunctionARN"] == func:
            return True
    return False


def attach_function():
    """ Attach or update the function connected to the distribution """
    # Get the function ARN without the version number in it
    func = get_lambda_arn()
    no_ver = func.rsplit(":", 1)[0]

    item_block = {
        "EventType": "origin-response",
        "LambdaFunctionARN": func
    }
    session = boto3.Session()
    cf_client = session.client('cloudfront', 'us-east-1')
    config = cf_client.get_distribution_config(
        Id=get_env_var(_CFDIST)
    )
    distrib_config = config["DistributionConfig"]
    dcb = distrib_config["DefaultCacheBehavior"]
    if "LambdaFunctionAssociations" not in dcb:
        dcb["LambdaFunctionAssociations"] = {
            "Items": [
                item_block
            ],
            "Quantity": 1
        }
        print("Initialising LFA block to add security headers function")
    else:
        found = False
        if "Items" not in dcb["LambdaFunctionAssociations"]:
            dcb["LambdaFunctionAssociations"]["Items"] = []
        else:
            for lfa in dcb["LambdaFunctionAssociations"]["Items"]:
                if lfa["LambdaFunctionARN"].startswith(no_ver):
                    lfa["LambdaFunctionARN"] = func
                    found = True
                    print("Updating existing security headers function")
                    break
        if not found:
            lfa_block = dcb["LambdaFunctionAssociations"]
            lfa_block["Items"].append(item_block)
            lfa_block["Quantity"] = lfa_block["Quantity"] + 1
            print(
                "Adding security headers function, total of %s" %
                lfa_block["Quantity"])
    cf_client.update_distribution(
        DistributionConfig=distrib_config,
        Id=get_env_var(_CFDIST),
        IfMatch=config["ETag"]
    )
    print("CloudFront distribution updated")


if __name__ == '__main__':
    if is_function_attached():
        print("Security headers function is already attached")
    else:
        attach_function()
