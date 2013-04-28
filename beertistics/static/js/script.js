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

$(document).ready(function() {
    $.getJSON("/api/friends/")
    .done(function(data) {
        $("#active-user-input").typeahead({
            minLength: 3,
            source: data,
            sorter: function (items) {
                // in order to have exact typed match first among suggestions
                items.unshift(this.query); 
                return items;
            }
        });
    });    
});