function create_instance_selector_widget(opts) {
    const widget_root = $('#' + opts.widget_id);
    const field_input = $('#' + opts.input_id);
    const display_edit_link = widget_root.find('.js-instance-selector-widget-display-edit-link');
    const display_markup_wrap = widget_root.find('.js-instance-selector-widget-display-wrap');
    const trigger_button = widget_root.find('.js-instance-selector-widget-trigger');
    const edit_button = widget_root.find('.js-instance-selector-widget-edit');
    const clear_button = widget_root.find('.js-instance-selector-widget-clear');

    if (!widget_root.length) throw new Error(`Cannot find instance selector widget \`#${opts.widget_id}\``);
    if (!display_markup_wrap.length) throw new Error(`Cannot find instance selector widget display markup wrap in \`#${opts.widget_id}\``);
    if (!field_input.length) throw new Error(`Cannot find instance selector widget field input in \`#${opts.widget_id}\``);
    if (!trigger_button.length) throw new Error(`Cannot find instance selector widget trigger button in \`#${opts.widget_id}\``);
    if (!edit_button.length) throw new Error(`Cannot find instance selector widget edit button in \`#${opts.widget_id}\``);

    let modal;
    let is_loading = false;

    trigger_button.on('click', function() {
        if (is_loading) {
            return;
        }

        enter_loading_state();

        // Remove any previous modals
        $('body > .modal').remove();

        modal = $(`
            <div class="modal fade instance-selector-widget-modal" tabindex="-1" role="dialog" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content instance-selector-widget-modal__content">
                        <button type="button" class="button close icon text-replace icon-cross" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <div class="modal-body instance-selector-widget-modal__body">
                            <iframe class="instance-selector-widget-modal__embed" src="${opts.embed_url}" frameborder="0"></iframe>                        
                        </div>
                    </div>
                </div>
            </div>
        `);

        modal.find('iframe').on('load', () => {
            exit_loading_state();
            show_modal();
        });

        $('body').append(modal);
    });

    clear_button.on('click', () => {
        set_value({
            pk: '',
        });
    });

    window.addEventListener('message', message => {
        if (message.data && message.data.source === opts.embed_id) {
            const object_pk = message.data.object_pk;
            if (!object_pk) {
                throw new Error('`object_pk` was not provided by embed. Received: ' + JSON.stringify(message.data));
            }

            enter_loading_state();
            hide_modal();

            const lookup_url = `${opts.lookup_url}?${opts.OBJECT_PK_PARAM}=${object_pk}`;
            $.get({
                url: lookup_url,
                error: function(err) {
                    exit_loading_state();
                    console.error(err);
                },
                success: function(data) {
                    exit_loading_state();
                    set_value(data);
                }
            });
        }
    });

    function show_modal() {
        modal.modal('show');
    }

    function hide_modal() {
        modal.modal('hide');
    }

    function enter_loading_state() {
        is_loading = true;
        widget_root.addClass('instance-selector-widget--is-loading');
        widget_root.removeClass('instance-selector-widget--not-loading');
    }

    function exit_loading_state() {
        is_loading = false;
        widget_root.removeClass('instance-selector-widget--is-loading');
        widget_root.addClass('instance-selector-widget--not-loading');
    }

    function set_value(data) {
        field_input.val(data.pk);

        display_markup_wrap.html(data.display_markup);
        display_edit_link.attr('href', data.edit_url || null);
        edit_button.attr('href', data.edit_url || null);

        if (data.pk) {
            widget_root
                .removeClass('instance-selector-widget--unselected')
                .addClass('instance-selector-widget--selected');
        } else {
            widget_root
                .addClass('instance-selector-widget--unselected')
                .removeClass('instance-selector-widget--selected');
        }
    }
}
