var beertistics = window.beertistics || {};

(function (ns) {
    "use strict";

    _.templateSettings.variable = "rc";

    function startLoading(el) {
        el.addClass('graph-container');
        el.append($("script.loading-template").html());
    }

    function stopLoading(el) {
        el.find(".loading").remove();
        el.removeClass("graph-container");
    }

    function stopLoadingWithError(el, msg) {
        stopLoading(el);
        var template = _.template($("script.loading-error-template").html());
        el.append(template({"message": msg}));
    }

    ns.loadData = function (url, element, success) {
            startLoading(element);
            $.getJSON(url)
                .done(function(data) {
                    stopLoading(element);
                    success(data);
                })
                .fail(function(error) {
                    stopLoadingWithError(element, error.responseText);
                });
    };

}(beertistics));