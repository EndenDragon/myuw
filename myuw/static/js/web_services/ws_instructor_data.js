function InstructorData(instructor_regid) {
    this.url = "/api/v1/person/" + instructor_regid;
    this.data = null;
    this.error = null;
}

InstructorData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructorData = InstructorData;
