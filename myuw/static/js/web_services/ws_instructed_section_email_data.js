function InstructedSectionEmailListData(section_label) {
    this.url = "/api/v1/emaillist/" + section_label;
    this.data = null;
    this.error = null;
}

InstructedSectionEmailListData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructedSectionEmailListData = InstructedSectionEmailListData;
