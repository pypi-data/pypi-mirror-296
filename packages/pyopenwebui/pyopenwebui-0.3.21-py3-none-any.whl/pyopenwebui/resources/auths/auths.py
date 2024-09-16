# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .admin import (
    AdminResource,
    AsyncAdminResource,
    AdminResourceWithRawResponse,
    AsyncAdminResourceWithRawResponse,
    AdminResourceWithStreamingResponse,
    AsyncAdminResourceWithStreamingResponse,
)
from ...types import (
    auth_add_params,
    auth_signin_params,
    auth_signup_params,
    auth_update_profile_params,
    auth_update_password_params,
)
from .api_key import (
    APIKeyResource,
    AsyncAPIKeyResource,
    APIKeyResourceWithRawResponse,
    AsyncAPIKeyResourceWithRawResponse,
    APIKeyResourceWithStreamingResponse,
    AsyncAPIKeyResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.signin_response import SigninResponse
from ...types.auth_list_response import AuthListResponse
from ...types.auth_update_profile_response import AuthUpdateProfileResponse
from ...types.auth_update_password_response import AuthUpdatePasswordResponse

__all__ = ["AuthsResource", "AsyncAuthsResource"]


class AuthsResource(SyncAPIResource):
    @cached_property
    def admin(self) -> AdminResource:
        return AdminResource(self._client)

    @cached_property
    def api_key(self) -> APIKeyResource:
        return APIKeyResource(self._client)

    @cached_property
    def with_raw_response(self) -> AuthsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AuthsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AuthsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuthListResponse:
        """Get Session User"""
        return self._get(
            "/auths/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthListResponse,
        )

    def add(
        self,
        *,
        email: str,
        name: str,
        password: str,
        profile_image_url: Optional[str] | NotGiven = NOT_GIVEN,
        role: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SigninResponse:
        """
        Add User

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auths/add",
            body=maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "password": password,
                    "profile_image_url": profile_image_url,
                    "role": role,
                },
                auth_add_params.AuthAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SigninResponse,
        )

    def signin(
        self,
        *,
        email: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SigninResponse:
        """
        Signin

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auths/signin",
            body=maybe_transform(
                {
                    "email": email,
                    "password": password,
                },
                auth_signin_params.AuthSigninParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SigninResponse,
        )

    def signup(
        self,
        *,
        email: str,
        name: str,
        password: str,
        profile_image_url: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SigninResponse:
        """
        Signup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auths/signup",
            body=maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "password": password,
                    "profile_image_url": profile_image_url,
                },
                auth_signup_params.AuthSignupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SigninResponse,
        )

    def update_password(
        self,
        *,
        new_password: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuthUpdatePasswordResponse:
        """
        Update Password

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auths/update/password",
            body=maybe_transform(
                {
                    "new_password": new_password,
                    "password": password,
                },
                auth_update_password_params.AuthUpdatePasswordParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthUpdatePasswordResponse,
        )

    def update_profile(
        self,
        *,
        name: str,
        profile_image_url: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuthUpdateProfileResponse:
        """
        Update Profile

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auths/update/profile",
            body=maybe_transform(
                {
                    "name": name,
                    "profile_image_url": profile_image_url,
                },
                auth_update_profile_params.AuthUpdateProfileParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthUpdateProfileResponse,
        )


class AsyncAuthsResource(AsyncAPIResource):
    @cached_property
    def admin(self) -> AsyncAdminResource:
        return AsyncAdminResource(self._client)

    @cached_property
    def api_key(self) -> AsyncAPIKeyResource:
        return AsyncAPIKeyResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAuthsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAuthsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncAuthsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuthListResponse:
        """Get Session User"""
        return await self._get(
            "/auths/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthListResponse,
        )

    async def add(
        self,
        *,
        email: str,
        name: str,
        password: str,
        profile_image_url: Optional[str] | NotGiven = NOT_GIVEN,
        role: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SigninResponse:
        """
        Add User

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auths/add",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "password": password,
                    "profile_image_url": profile_image_url,
                    "role": role,
                },
                auth_add_params.AuthAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SigninResponse,
        )

    async def signin(
        self,
        *,
        email: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SigninResponse:
        """
        Signin

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auths/signin",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "password": password,
                },
                auth_signin_params.AuthSigninParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SigninResponse,
        )

    async def signup(
        self,
        *,
        email: str,
        name: str,
        password: str,
        profile_image_url: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SigninResponse:
        """
        Signup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auths/signup",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "password": password,
                    "profile_image_url": profile_image_url,
                },
                auth_signup_params.AuthSignupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SigninResponse,
        )

    async def update_password(
        self,
        *,
        new_password: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuthUpdatePasswordResponse:
        """
        Update Password

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auths/update/password",
            body=await async_maybe_transform(
                {
                    "new_password": new_password,
                    "password": password,
                },
                auth_update_password_params.AuthUpdatePasswordParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthUpdatePasswordResponse,
        )

    async def update_profile(
        self,
        *,
        name: str,
        profile_image_url: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuthUpdateProfileResponse:
        """
        Update Profile

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auths/update/profile",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "profile_image_url": profile_image_url,
                },
                auth_update_profile_params.AuthUpdateProfileParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthUpdateProfileResponse,
        )


class AuthsResourceWithRawResponse:
    def __init__(self, auths: AuthsResource) -> None:
        self._auths = auths

        self.list = to_raw_response_wrapper(
            auths.list,
        )
        self.add = to_raw_response_wrapper(
            auths.add,
        )
        self.signin = to_raw_response_wrapper(
            auths.signin,
        )
        self.signup = to_raw_response_wrapper(
            auths.signup,
        )
        self.update_password = to_raw_response_wrapper(
            auths.update_password,
        )
        self.update_profile = to_raw_response_wrapper(
            auths.update_profile,
        )

    @cached_property
    def admin(self) -> AdminResourceWithRawResponse:
        return AdminResourceWithRawResponse(self._auths.admin)

    @cached_property
    def api_key(self) -> APIKeyResourceWithRawResponse:
        return APIKeyResourceWithRawResponse(self._auths.api_key)


class AsyncAuthsResourceWithRawResponse:
    def __init__(self, auths: AsyncAuthsResource) -> None:
        self._auths = auths

        self.list = async_to_raw_response_wrapper(
            auths.list,
        )
        self.add = async_to_raw_response_wrapper(
            auths.add,
        )
        self.signin = async_to_raw_response_wrapper(
            auths.signin,
        )
        self.signup = async_to_raw_response_wrapper(
            auths.signup,
        )
        self.update_password = async_to_raw_response_wrapper(
            auths.update_password,
        )
        self.update_profile = async_to_raw_response_wrapper(
            auths.update_profile,
        )

    @cached_property
    def admin(self) -> AsyncAdminResourceWithRawResponse:
        return AsyncAdminResourceWithRawResponse(self._auths.admin)

    @cached_property
    def api_key(self) -> AsyncAPIKeyResourceWithRawResponse:
        return AsyncAPIKeyResourceWithRawResponse(self._auths.api_key)


class AuthsResourceWithStreamingResponse:
    def __init__(self, auths: AuthsResource) -> None:
        self._auths = auths

        self.list = to_streamed_response_wrapper(
            auths.list,
        )
        self.add = to_streamed_response_wrapper(
            auths.add,
        )
        self.signin = to_streamed_response_wrapper(
            auths.signin,
        )
        self.signup = to_streamed_response_wrapper(
            auths.signup,
        )
        self.update_password = to_streamed_response_wrapper(
            auths.update_password,
        )
        self.update_profile = to_streamed_response_wrapper(
            auths.update_profile,
        )

    @cached_property
    def admin(self) -> AdminResourceWithStreamingResponse:
        return AdminResourceWithStreamingResponse(self._auths.admin)

    @cached_property
    def api_key(self) -> APIKeyResourceWithStreamingResponse:
        return APIKeyResourceWithStreamingResponse(self._auths.api_key)


class AsyncAuthsResourceWithStreamingResponse:
    def __init__(self, auths: AsyncAuthsResource) -> None:
        self._auths = auths

        self.list = async_to_streamed_response_wrapper(
            auths.list,
        )
        self.add = async_to_streamed_response_wrapper(
            auths.add,
        )
        self.signin = async_to_streamed_response_wrapper(
            auths.signin,
        )
        self.signup = async_to_streamed_response_wrapper(
            auths.signup,
        )
        self.update_password = async_to_streamed_response_wrapper(
            auths.update_password,
        )
        self.update_profile = async_to_streamed_response_wrapper(
            auths.update_profile,
        )

    @cached_property
    def admin(self) -> AsyncAdminResourceWithStreamingResponse:
        return AsyncAdminResourceWithStreamingResponse(self._auths.admin)

    @cached_property
    def api_key(self) -> AsyncAPIKeyResourceWithStreamingResponse:
        return AsyncAPIKeyResourceWithStreamingResponse(self._auths.api_key)
