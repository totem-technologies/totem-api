// This file is auto-generated by @hey-api/openapi-ts

import { type Options as ClientOptions, type TDataShape, type Client, formDataBodySerializer } from '@hey-api/client-fetch';
import type { TotemApiApiSecretData, TotemApiApiLoginData, TotemApiApiLoginResponse, TotemApiApiTokenData, TotemApiApiTokenResponse, TotemApiApiCurrentUserData, TotemApiApiCurrentUserResponse, TotemApiApiCurrentUserError, TotemApiApiUserAvatarUpdateData, TotemApiApiUserAvatarUpdateError, TotemApiApiUserUploadProfileImageData, TotemApiApiUserUploadProfileImageError, TotemCirclesApiListEventsData, TotemCirclesApiListEventsResponse, TotemCirclesApiFilterOptionsData, TotemCirclesApiFilterOptionsResponse, TotemCirclesApiEventDetailData, TotemCirclesApiEventDetailResponse, TotemCirclesApiUpcomingEventsData, TotemCirclesApiUpcomingEventsResponse, TotemCirclesApiWebflowEventsListData, TotemCirclesApiWebflowEventsListResponse } from './types.gen';
import { client as _heyApiClient } from './client.gen';

export type Options<TData extends TDataShape = TDataShape, ThrowOnError extends boolean = boolean> = ClientOptions<TData, ThrowOnError> & {
    /**
     * You can provide a client instance returned by `createClient()` instead of
     * individual options. This might be also useful if you want to implement a
     * custom client.
     */
    client?: Client;
    /**
     * You can pass arbitrary values through the `meta` object. This can be
     * used to access values that aren't defined as part of the SDK function.
     */
    meta?: Record<string, unknown>;
};

/**
 * Secret
 */
export const totemApiApiSecret = <ThrowOnError extends boolean = false>(options?: Options<TotemApiApiSecretData, ThrowOnError>) => {
    return (options?.client ?? _heyApiClient).get<unknown, unknown, ThrowOnError>({
        security: [
            {
                name: 'X-API-Key',
                type: 'apiKey'
            }
        ],
        url: '/api/v1/protected',
        ...options
    });
};

/**
 * Login
 */
export const totemApiApiLogin = <ThrowOnError extends boolean = false>(options: Options<TotemApiApiLoginData, ThrowOnError>) => {
    return (options.client ?? _heyApiClient).post<TotemApiApiLoginResponse, unknown, ThrowOnError>({
        url: '/api/v1/auth/login',
        ...options
    });
};

/**
 * Token
 */
export const totemApiApiToken = <ThrowOnError extends boolean = false>(options: Options<TotemApiApiTokenData, ThrowOnError>) => {
    return (options.client ?? _heyApiClient).post<TotemApiApiTokenResponse, unknown, ThrowOnError>({
        url: '/api/v1/auth/token',
        ...options
    });
};

/**
 * Current User
 */
export const totemApiApiCurrentUser = <ThrowOnError extends boolean = false>(options?: Options<TotemApiApiCurrentUserData, ThrowOnError>) => {
    return (options?.client ?? _heyApiClient).get<TotemApiApiCurrentUserResponse, TotemApiApiCurrentUserError, ThrowOnError>({
        url: '/api/v1/auth/currentuser',
        ...options
    });
};

/**
 * User Avatar Update
 */
export const totemApiApiUserAvatarUpdate = <ThrowOnError extends boolean = false>(options: Options<TotemApiApiUserAvatarUpdateData, ThrowOnError>) => {
    return (options.client ?? _heyApiClient).post<unknown, TotemApiApiUserAvatarUpdateError, ThrowOnError>({
        url: '/api/v1/user/avatarupdate',
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers
        }
    });
};

/**
 * User Upload Profile Image
 */
export const totemApiApiUserUploadProfileImage = <ThrowOnError extends boolean = false>(options: Options<TotemApiApiUserUploadProfileImageData, ThrowOnError>) => {
    return (options.client ?? _heyApiClient).post<unknown, TotemApiApiUserUploadProfileImageError, ThrowOnError>({
        ...formDataBodySerializer,
        url: '/api/v1/user/avatarimage',
        ...options,
        headers: {
            'Content-Type': null,
            ...options?.headers
        }
    });
};

/**
 * List Events
 */
export const totemCirclesApiListEvents = <ThrowOnError extends boolean = false>(options: Options<TotemCirclesApiListEventsData, ThrowOnError>) => {
    return (options.client ?? _heyApiClient).get<TotemCirclesApiListEventsResponse, unknown, ThrowOnError>({
        url: '/api/v1/spaces/',
        ...options
    });
};

/**
 * Filter Options
 */
export const totemCirclesApiFilterOptions = <ThrowOnError extends boolean = false>(options?: Options<TotemCirclesApiFilterOptionsData, ThrowOnError>) => {
    return (options?.client ?? _heyApiClient).get<TotemCirclesApiFilterOptionsResponse, unknown, ThrowOnError>({
        url: '/api/v1/spaces/filter-options',
        ...options
    });
};

/**
 * Event Detail
 */
export const totemCirclesApiEventDetail = <ThrowOnError extends boolean = false>(options: Options<TotemCirclesApiEventDetailData, ThrowOnError>) => {
    return (options.client ?? _heyApiClient).get<TotemCirclesApiEventDetailResponse, unknown, ThrowOnError>({
        url: '/api/v1/spaces/event/{event_slug}',
        ...options
    });
};

/**
 * Upcoming Events
 */
export const totemCirclesApiUpcomingEvents = <ThrowOnError extends boolean = false>(options?: Options<TotemCirclesApiUpcomingEventsData, ThrowOnError>) => {
    return (options?.client ?? _heyApiClient).get<TotemCirclesApiUpcomingEventsResponse, unknown, ThrowOnError>({
        url: '/api/v1/spaces/calendar',
        ...options
    });
};

/**
 * Webflow Events List
 */
export const totemCirclesApiWebflowEventsList = <ThrowOnError extends boolean = false>(options?: Options<TotemCirclesApiWebflowEventsListData, ThrowOnError>) => {
    return (options?.client ?? _heyApiClient).get<TotemCirclesApiWebflowEventsListResponse, unknown, ThrowOnError>({
        url: '/api/v1/spaces/webflow/list_events',
        ...options
    });
};