(function() {
    const IS_EMBEDDED = window.parent && window.parent !== window;
    const IS_INSTANCE_SELECTOR_EMBED = IS_EMBEDDED
        ? window.parent.location.pathname.indexOf('/instance-selector/') !== -1
        : false;

    const SESSION_STORAGE_EMBED_KEY = 'INSTANCE_SELECTOR_EMBED_ID';

    if (IS_INSTANCE_SELECTOR_EMBED) {
        const HASH_EMBED_ID = window.location.hash.split('#instance_selector_embed_id:')[1];
        // Persist embed id across page loads (allows clicking on filters, searching, etc)
        const SESSION_EMBED_ID = sessionStorage.getItem(SESSION_STORAGE_EMBED_KEY);
        if (HASH_EMBED_ID) {
            sessionStorage.setItem(SESSION_STORAGE_EMBED_KEY, HASH_EMBED_ID);
        }

        const EMBED_ID = HASH_EMBED_ID || SESSION_EMBED_ID;
        if (!EMBED_ID) {
            throw new Error('`EMBED_ID` cannot be determined');
        }

        // Poll for earliest access to the body so that we can effect the styles before
        // complete page load
        setTimeout(_poll_for_body, 0);
        function _poll_for_body() {
            if (!document.body) {
                setTimeout(_poll_for_body, 0);
                return;
            }
            document.body.classList.add('is-instance-selector-embed');
        }

        document.addEventListener('DOMContentLoaded', function() {
            const listing = $('.listing');

            const items = listing.find('tbody tr');
            items.on('click', 'a', function(event) {
                event.preventDefault();
                let href = this.href;
                if (!href) {
                    const actions = items.find('.actions').has(this);
                    href = actions.find('a[href]')[0].href;
                }
                const data = get_data_from_url(href);
                if (!data) {
                    throw new Error('Cannot find object PK from url');
                }
                handle_object_pk_selected(data.object_pk);
            });

            const actions = items.find('.actions');
            const select_button = $(
                '<li class="instance-selector__select-button">' +
                    '<a class="button button-secondary button-small" title="Select this object">Select</a>' +
                '</li>'
            );
            actions.append(select_button);

            $(document.body).on('click', '.js-instance-selector-target', function(event) {
                event.preventDefault();
                const object_pk = $(this).data('instance-selector-pk');
                if (!object_pk) {
                    console.error('Cannot find `instance-selector-pk` value', this);
                    throw new Error('Cannot find `instance-selector-pk` value.');
                }
                handle_object_pk_selected(object_pk);
            });

            // Allow users to select items referenced in creation success messages
            const success_messages = $('.messages .success');
            success_messages.each(function() {
                const success_message = $(this);
                
                const buttons = success_message.find('.buttons a');
                buttons.each(function() {
                    const button = $(this);
                    const button_text = button.text().trim();
                    if (button_text.toLowerCase() === 'edit') {
                        const url = button.attr('href');
                        const data = get_data_from_url(url);
                        if (data) {
                            const select_button = $(`
                                <a 
                                    class="button button-small button-secondary instance-selector__success-message__select-button"
                                    data-object-pk-for-debugging="${data.object_pk}"
                                >Select</a>
                            `);
                            button.parent().prepend(select_button);
                            select_button.on('click', function(event) {
                                event.preventDefault();
                                handle_object_pk_selected(data.object_pk);
                            });
                        }
                    }
                });
            });

        });

        const index_view_url = window.location.pathname;
        function get_data_from_url(url) {
            const url_subpath = url.split(index_view_url)[1];
            const url_subpath_tokens = url_subpath.split('/');
            const view_name = url_subpath_tokens[0];
            const object_pk = url_subpath_tokens[1];
            const pk = object_pk ? object_pk : view_name;

            return {
                view_name: view_name,
                object_pk: pk,
            };
        }

        function handle_object_pk_selected(object_pk) {
            // Embed session writes persist into the parent's session
            sessionStorage.removeItem(SESSION_STORAGE_EMBED_KEY);

            const message = {
                'source': EMBED_ID,
                'object_pk': object_pk,
            };
            window.parent.postMessage(message, location.origin);
        }
    }
})();
