"""
# File       : api_errors.py
# Time       ：2024/8/22 09:39
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from fastapi import HTTPException


class HTTPException_AppToolsSZXW(HTTPException):
    """自定义异常类"""

    def __init__(self, error_code: int,
                 detail: str,
                 http_status_code: int = 404):
        super().__init__(http_status_code,
                         detail={"error_code": error_code,
                                 "detail": detail})


class ErrorCode:
    """错误码"""
    支付宝支付接口调用失败 = 500001
    签名验证失败 = 500002
    商户订单号不能为空或超过32位 = 500003
    价格不能为空或小于0 = 500004
    商品名称不能为空 = 500005
    EXCEPTION = 3
    WARNING = 4
    INFO = 5
    DEBUG = 6
    # 新增错误码
    用户未找到 = 404001
    角色未找到 = 404002
    无效的刷新令牌 = 401001
    刷新令牌已过期 = 401002
    微信登录失败 = 400006
    生成二维码失败 = 500006
    用户名已注册 = 400001
    手机号已注册 = 400002
    无效的手机号或验证码 = 400003
    无效的邮箱或验证码 = 400004
    无效的用户名或密码 = 400005
    应用未找到 = 403001
    权限不足 = 403002
