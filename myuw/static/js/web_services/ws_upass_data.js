function UPassData() {
    this.url = "/api/v1/upass/";
    this.data = null;
    this.error = null;
}

UPassData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.UPassData = UPassData;
