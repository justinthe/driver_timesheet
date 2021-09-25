package com.example.driver_management;


import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Approval {

    private int timesheetId;
    private int approverId;
    private Date dttimeenter;
    private boolean approved;
    private boolean inout;
    private String str_inout;
    private DateFormat dtFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");


    public Approval(int timesheetId, int approverId, Date dttimeenter, boolean inout) {
        this.timesheetId = timesheetId;
        this.approverId = approverId;
        this.dttimeenter = dttimeenter;
        this.inout = inout;
        setInout(inout);
    }

    public int getTimesheetId() {
        return timesheetId;
    }

    public void setTimesheetId(int timesheetId) {
        this.timesheetId = timesheetId;
    }

    public int getApproverId() {
        return approverId;
    }

    public void setApproverId(int approverId) {
        this.approverId = approverId;
    }

    public Date getDttimeenter() { return dttimeenter; }

    public String getStrDttimeenter() { return dtFormat.format(dttimeenter); }

    public void setDttimeenter(Date dttimeenter) {
        this.dttimeenter = dttimeenter;
    }

    public boolean isApproved() {
        return approved;
    }

    public void setApproved(boolean approved) {
        this.approved = approved;
    }

    public boolean isInout() {
        return inout;
    }

    public void setInout(boolean inout) {
        this.inout = inout;
        if (inout) {
            setStr_inout("in");
        } else {
            setStr_inout("out");
        }
    }

    public String getStr_inout() {
       return str_inout;
    }

    public void setStr_inout(String str_inout) {
        this.str_inout = str_inout;
    }
}
