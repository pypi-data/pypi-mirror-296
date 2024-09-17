class LogEvents:
    @staticmethod
    def log_event(severity="info", event_type=None, payload=None, print_to_console=True):
        # `event_sender` module is defined in `lumeopython` GStreamer element, so it's not available
        # during Python unit tests.
        import event_sender

        available_severities = ["debug", "info", "warning", "error"]

        if severity not in available_severities:
            raise ValueError("'severity' value is not in {}".format(available_severities))

        if not event_type:
            raise ValueError("'event_type' is empty or missing")

        if not payload:
            raise ValueError("'payload' is empty or missing")

        event_sender.send(severity, event_type, payload)

        if print_to_console:
            print(f"Event: {severity} - {event_type} - {payload}")


    @staticmethod
    def error_log(object_to_log, node_id=""):
        print("{} Error : {}".format(node_id, object_to_log))
        LogEvents.log_event("error", "deployment.error.node", f"{node_id} Error : {object_to_log}")


    @staticmethod
    def warning_log(object_to_log, node_id=""):
        print("{} Warning : {}".format(node_id, object_to_log))
        LogEvents.log_event("warning", "deployment.warning.node", f"{node_id} Warning : {object_to_log}")


    @staticmethod
    def info_log(object_to_log, node_id=""):
        print("{} Info : {}".format(node_id, object_to_log))
        LogEvents.log_event("info", "deployment.info.node", f"{node_id} : {object_to_log}")


    @staticmethod
    def debug_log(object_to_log, node_id=""):
        print("{} : {}".format(node_id, object_to_log))
        LogEvents.log_event("debug", "deployment.debug.node", f"{node_id} : {object_to_log}")


    @staticmethod
    def conditional_debug_log(object_to_log, condition, node_id=""):
        if condition:
            print("{} : {}".format(node_id, object_to_log))


# Expose methods at the module level
#     This is necessary if you want to import these methods directly from log_events.py without referencing the LogEvents class.
#     This setup allows you to re-export these methods in the __init__.py file of the utils module, making them directly
#     accessible when importing from lumeo.utils.
log_event = LogEvents.log_event
error_log = LogEvents.error_log
warning_log = LogEvents.warning_log
info_log = LogEvents.info_log
debug_log = LogEvents.debug_log
conditional_debug_log = LogEvents.conditional_debug_log