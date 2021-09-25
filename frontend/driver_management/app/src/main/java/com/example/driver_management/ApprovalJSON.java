package com.example.driver_management;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class ApprovalJSON {

    @SerializedName("timesheets")
    List<Timesheet> timesheets;

    @SerializedName("success")
    String success;

    @SerializedName("total_records")
    int totalRecords;

    class Timesheet {

        @SerializedName("dttimeenter")
        String dttimeenter;

        @SerializedName("inout")
        Boolean inout;

        @SerializedName("timesheetid")
        int timesheetid;

        @SerializedName("userid")
        int userid;
    }
}
