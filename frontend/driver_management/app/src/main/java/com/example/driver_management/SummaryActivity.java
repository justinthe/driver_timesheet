package com.example.driver_management;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.os.RecoverySystem;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class SummaryActivity extends AppCompatActivity {

    private static String TAG = "SummaryActivity";

    private ApprovalAdapter adapter;
    private ArrayList<Approval> approvalArrayList;

    private RecyclerView recyclerView;
    private Button btnApprove;
    private Button btnReject;
    private EditText eTextStartDate;

    final Calendar myCalendar = Calendar.getInstance();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_summary);

        addData();

        btnApprove = (Button) findViewById(R.id.buttonApprove);
        btnReject = (Button) findViewById(R.id.buttonReject);

        recyclerView = (RecyclerView) findViewById(R.id.recyclerView);
        adapter = new ApprovalAdapter(approvalArrayList);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(SummaryActivity.this);
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setAdapter(adapter);

        eTextStartDate = (EditText) findViewById(R.id.textboxStartdate);
        DatePickerDialog.OnDateSetListener date = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                myCalendar.set(Calendar.YEAR, i);
                myCalendar.set(Calendar.MONTH, i1);
                myCalendar.set(Calendar.DAY_OF_MONTH, i2);
                updateLabel();
            }
        };



        btnApprove.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.d(TAG, "Datalist.length: " + approvalArrayList.size());
                for (int i = 0; i < approvalArrayList.size(); i++) {
                    Approval app = approvalArrayList.get(i);
                    Log.d(TAG, "Timesheetid: " + app.getTimesheetId() + "; approval: " + app.isApproved());
                }
            }
        });

        eTextStartDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new DatePickerDialog(SummaryActivity.this, date, myCalendar.get(Calendar.YEAR),
                        myCalendar.get(Calendar.MONTH), myCalendar.get(Calendar.DAY_OF_MONTH)).show();
            }
        });
    }

    private void updateLabel() {
        String myFormat = "yyyy/MM/dd";
        SimpleDateFormat sdf = new SimpleDateFormat(myFormat, Locale.getDefault());
        eTextStartDate.setText(sdf.format(myCalendar.getTime()));
    }

    protected void addData() {
        approvalArrayList = new ArrayList<>();
        DateFormat format = new SimpleDateFormat("yyyy/MMM/dd HH:mm:ss");
        String str_dt1 = "2021/Jul/20 07:10:00";
        String str_dt2 = "2021/Jul/20 18:22:00";
        Date dt1 = new Date();
        Date dt2 = new Date();
        try {
            dt1 = format.parse(str_dt1);
            dt2 = format.parse(str_dt2);
        }
        catch(ParseException e) {
            e.printStackTrace();
        }

        approvalArrayList.add(new Approval(1, 23, dt1, true));
        approvalArrayList.add(new Approval(2, 23, dt2, false));
    }
}