var beertistics = window.beertistics || {};

(function (ns) {
    "use strict";

    _.templateSettings.variable = "rc";

    ns.startLoading = function (el) {
        el.addClass('graph-container');
        el.append($("script.loading-template").html());
    };

    ns.stopLoading = function (el) {
        el.find(".loading").remove();
        el.removeClass("graph-container");
    };

    ns.stopLoadingWithError = function (el, msg) {
        ns.stopLoading(el);
        var template = _.template($("script.loading-error-template").html());
        el.append(template({"message": msg}));
    };

}(beertistics));