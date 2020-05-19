from instance_selector.utils import user_can_access_admin


def XFrameOptionsMiddleware(get_response):
    def instance_selector_xframe_options_middleware(request):
        """
        If the X_FRAME_OPTIONS setting is set to `DENY`, it will cause most browsers to
        reject instance selector's iframes. This middleware looks for admin users
        that are using embed and flags that the response can be used within an iframe
        """
        response = get_response(request)

        if (
            response.get('X-Frame-Options').upper() == 'DENY'
            and user_can_access_admin(request.user)
        ):
            response['X-Frame-Options'] = 'SAMEORIGIN'
        return response

    return instance_selector_xframe_options_middleware
