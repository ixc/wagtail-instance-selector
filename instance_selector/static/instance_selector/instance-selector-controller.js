class InstanceSelectorController extends window.StimulusModule.Controller {
    static values = { config: Object };

    connect() {
        create_instance_selector_widget(this.configValue);
        console.log(this.configValue);
    }
}

window.wagtail.app.register('instance-selector', InstanceSelectorController);
