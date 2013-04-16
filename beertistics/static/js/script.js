function startLoading(el) {
    el.addClass('graph-container');
    el.append($("script.loading-template").html());
}

function stopLoading(el) {
    el.find(".loading").remove();
}