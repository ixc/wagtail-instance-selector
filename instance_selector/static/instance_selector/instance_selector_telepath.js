(function() {
    function InstanceSelector(html, config) {
        this.html = html;
        this.baseConfig = config;
    }
    InstanceSelector.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;
        var config = {};
        // replace __NAME__ and __ID__ placeholders in config with the real name / id
        for (prop in this.baseConfig) {
            config[prop] = this.baseConfig[prop].replace(/__NAME__/g, name).replace(/__ID__/g, id);;
        }

        // Set the config attribute on the input element so the controller can find it
        var inputElement = document.getElementById(id);
        if (inputElement) {
            inputElement.setAttribute('data-instance-selector-config-value', JSON.stringify(config));
        }

        var chooser = create_instance_selector_widget(config);
        chooser.setState(initialState);
        return chooser;
    };

    window.telepath.register('wagtailinstanceselector.widgets.InstanceSelector', InstanceSelector);
})();
