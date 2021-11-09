package com.example.driver_management;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.Toast;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.JSONObjectRequestListener;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.Executors;
/**************************************************************************************************
*
* - Calling API to populate the recyclerview.
* - Calling method is put into a separate thread (addData() method,
*   which calls GetDataFromAPI() class)
* - First time it loads, it does not send either dtstart and dtend.
 *  API is smart enough to generate the return list when no date start and date end provided.
 *  Default date range is current monday to friday.
* - Possible improvements:
*   1. default date start and date end
*
**************************************************************************************************/


public class ApprovalActivity extends AppCompatActivity {


    private static String TAG = "ApprovalActivity";

    private ApprovalAdapter adapter;
    private ArrayList<Approval> approvalArrayList;

    private RecyclerView recyclerView;
    private Button btnApprove;
    private Button btnReject;
    private Button btnRun;
    private EditText eTextStartDate;
    private EditText eTextEndDate;

    final Calendar myCalendar = Calendar.getInstance();
    private String api_url;
    private String bulk_approve_api_url;

    Map<String, String> pMap = new HashMap<String, String>();

    private Handler mainHandler = new Handler();
    private volatile boolean stopAddDataThread = false;
    private volatile boolean stopBulkApproveThread = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_approval);
        AndroidNetworking.initialize(getApplicationContext());

        api_url = getString(R.string.url_get_timesheet);
        bulk_approve_api_url = getString(R.string.bulk_approve_api_url);
        pMap.put("needapprovedonly", "True");
        approvalArrayList = new ArrayList<>();

        generateData();

        btnApprove = (Button) findViewById(R.id.buttonApprove);
        btnReject = (Button) findViewById(R.id.buttonReject);
        btnRun = (Button) findViewById(R.id.buttonRun);

        recyclerView = (RecyclerView) findViewById(R.id.recyclerView);
//        Log.d(TAG, "approvalArrayList size: " + approvalArrayList.size());
        adapter = new ApprovalAdapter(approvalArrayList);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(ApprovalActivity.this);
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setAdapter(adapter);

        eTextStartDate = (EditText) findViewById(R.id.textboxStartdate);
        DatePickerDialog.OnDateSetListener sDate = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                myCalendar.set(Calendar.YEAR, i);
                myCalendar.set(Calendar.MONTH, i1);
                myCalendar.set(Calendar.DAY_OF_MONTH, i2);
                updateLabel(eTextStartDate);
            }
        };

        eTextEndDate = (EditText) findViewById(R.id.textboxEnddate);
        DatePickerDialog.OnDateSetListener eDate = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                myCalendar.set(Calendar.YEAR, i);
                myCalendar.set(Calendar.MONTH, i1);
                myCalendar.set(Calendar.DAY_OF_MONTH, i2);
                updateLabel(eTextEndDate);
            }
        };


        btnApprove.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                Log.d(TAG, "Datalist.length: " + approvalArrayList.size());
                String approverId = null;
                for (int i = 0; i < approvalArrayList.size(); i++) {
                    Approval app = approvalArrayList.get(i);
                    approverId = Integer.toString(app.getApproverId());
                    Log.d(TAG, "Timesheetid: " + app.getTimesheetId() + "; approval: " + app.isApproved() + "; id: " + app.getApproverId());
                }

                approveTimesheets(approverId);
            }
        });

        btnRun.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String sDate = eTextStartDate.getText().toString();
                String eDate = eTextEndDate.getText().toString();
                Log.d(TAG, "onClick: - Start: " + sDate + "; End: " + eDate);
                pMap.put("dtstart", sDate);
                pMap.put("dtend", eDate);

                generateData();
            }
        });

        eTextStartDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new DatePickerDialog(ApprovalActivity.this, sDate, myCalendar.get(Calendar.YEAR),
                        myCalendar.get(Calendar.MONTH), myCalendar.get(Calendar.DAY_OF_MONTH)).show();
            }
        });

        eTextEndDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new DatePickerDialog(ApprovalActivity.this, eDate, myCalendar.get(Calendar.YEAR),
                        myCalendar.get(Calendar.MONTH), myCalendar.get(Calendar.DAY_OF_MONTH)).show();
            }
        });
    }

    private void updateLabel(EditText pToChange) {
        String myFormat = "yyyy-MM-dd";
        SimpleDateFormat sdf = new SimpleDateFormat(myFormat, Locale.getDefault());
        pToChange.setText(sdf.format(myCalendar.getTime()));
    }

    protected void approveTimesheets(String approverId) {
        BulkApproveAPI runnable = new BulkApproveAPI(approvalArrayList, bulk_approve_api_url, approverId);
        new Thread(runnable).start();
    }

    class BulkApproveAPI extends Thread {
        ArrayList<Approval> approvalArrayList;
        String bulk_approve_api_url;
//        String approverId;

        BulkApproveAPI(ArrayList approvalArrayList, String bulk_approve_api_url, String approverId) {
            this.approvalArrayList = approvalArrayList;
//            this.approverId = approverId;
            this.bulk_approve_api_url = bulk_approve_api_url + approverId;

        }

        @Override
        public void run() {
            Log.d(TAG, "run: API : " + bulk_approve_api_url);

            String jsonStr = new String();
            ArrayList<Integer> itemsToRemove = new ArrayList<Integer>();
            jsonStr = "[";

            for (int i = 0; i < approvalArrayList.size(); i++) {
                Approval app = approvalArrayList.get(i);

                if (app.isApproved()) {
                    jsonStr = jsonStr + "{\"timesheetid\":" + app.getTimesheetId() +
                            ", \"approved\":" + app.isApproved() + "},";
                    itemsToRemove.add(i);
                }
            }

            jsonStr = jsonStr.substring(0, jsonStr.length()-1);
            jsonStr += "]";
            Log.d(TAG, "jsonStr: " + jsonStr);

            JSONArray array = null;
            try {
                array = new JSONArray(jsonStr);
            } catch (JSONException e) {
                Log.d(TAG, "run: " + e.getMessage());
//                e.printStackTrace();
            }
//            Log.d(TAG, "jsonbody: " + array.toString() );

            AndroidNetworking.post(bulk_approve_api_url)
                                .addJSONArrayBody(array)
                                .setPriority(Priority.MEDIUM)
                                .build()
                                .getAsJSONObject(new JSONObjectRequestListener() {
                                    @Override
                                    public void onResponse(JSONObject response) {
                                        Toast.makeText(getApplicationContext(), "Success", Toast.LENGTH_SHORT).show();
                                        Log.d(TAG, "onResponse: " + response);
                                    }

                                    @Override
                                    public void onError(ANError anError) {
                                        Log.d(TAG, "onError: " + anError.getErrorDetail());
                                    }
                                });
            /*
            TODO:
            update UI
            notifyItemRemoved(int position)
            */

//            addData();
//            Log.d(TAG, "run bulk approve 1: " + approvalArrayList.size());
//            Log.d(TAG, "run itemstoremove size: " + itemsToRemove.size());
//            for (int i = 0; i < itemsToRemove.size(); i++) {
//                Log.d(TAG, "itemsToRemove: " + itemsToRemove.get(i));
//                Approval app = approvalArrayList.get(itemsToRemove.get(i));
//                Log.d(TAG, "toberemoved: " + app.getTimesheetId());
//                approvalArrayList.remove(app);
////                        adapter.notifyItemRemoved(itemsToRemove.get(i));
////                        adapter.notifyItemRemoved(i);
//            }
//            Log.d(TAG, "run bulk approve 2: " + approvalArrayList.size());
//            runOnUiThread(new Runnable() {
//                @Override
//                public void run() {
//                    Log.d(TAG, "run bulk approve: " + approvalArrayList.size() );
//                    adapter.notifyDataSetChanged();
////                    recyclerView.invalidate();
//                }
//            });
            generateData();
        }
    }

    protected void generateData() {
//        https://github.com/amitshekhariitbhu/Fast-Android-Networking/issues/34
//          setExecutore(Executors.newSingleThreadExecutor()) --> if not, data is not filled
        approvalArrayList.clear();
        stopAddDataThread = false;
        GetDataFromAPI runnable = new GetDataFromAPI(approvalArrayList, api_url, pMap);
        new Thread(runnable).start();
    }

    public void setStopAddDataThread(View view) {
        stopAddDataThread = true;
    }


    class GetDataFromAPI extends Thread {

        ArrayList<Approval> approvalArrayList;
        String api_url;
        Map<String, String> pMap;

        GetDataFromAPI(ArrayList approvalArrayList, String api_url, Map pMap) {
            this.approvalArrayList = approvalArrayList;
            this.api_url = api_url;
            this.pMap = pMap;
        }

        @Override
        public void run() {
            Log.d(TAG, "Calling API....." + api_url);
            Log.d(TAG, "pMap size: " + pMap.size());
            Log.d(TAG, "addData: " + approvalArrayList.size());
            Log.d(TAG, "run: sdate - " + pMap.get("dtstart") + "; edate - " + pMap.get("dtend"));

            AndroidNetworking.get(api_url)
                    .addQueryParameter(pMap)
                    .setPriority(Priority.MEDIUM)
                    .setExecutor(Executors.newSingleThreadExecutor())   // need this line otherwise data is not filled when showing
                    .build()
                    .getAsJSONObject(new JSONObjectRequestListener() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Log.d(TAG, "response: " + response);
                            Gson gson = new Gson();
                            ApprovalJSON approvalJSON = gson.fromJson(String.valueOf(response), ApprovalJSON.class);
                            List tsheet = approvalJSON.timesheets;
                            Log.d(TAG, "onResponse: Timesheets size - " + tsheet.size());
                            for (int i = 0; i < tsheet.size(); i++) {
                                ApprovalJSON.Timesheet ts = (ApprovalJSON.Timesheet) tsheet.get(i);
                                Boolean respInout = ts.inout;
                                int respTimesheetid = ts.timesheetid;
                                int respUserid = ts.userid;
                                String respStr_dt = ts.dttimeenter.substring(0, ts.dttimeenter.length() -4);    // remove GMT from the datetime
                                DateFormat sdf = new SimpleDateFormat("EEE, d MMM yyyy HH:mm:ss");
                                Date dt = new Date();
                                try {
                                    dt = sdf.parse(respStr_dt);
                                } catch (ParseException e) {
                                    Log.d(TAG, "onResponse: Error - " + e.getMessage());
                                }

                                approvalArrayList.add(new Approval(respTimesheetid,
                                                                    respUserid,
                                                                    dt,
                                                                    respInout)
                                                        );

                                // notify main thread list has changed
                                runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        Log.d(TAG, "notifyDatasetChanged");
                                        recyclerView.setAdapter(null);
                                        recyclerView.setAdapter(adapter);
                                        adapter.notifyDataSetChanged();
                                        recyclerView.invalidate();
                                        recyclerView.getRecycledViewPool().clear();
                                    }
                                });
                            }
                        }


                        @Override
                        public void onError(ANError anError) {
                            Log.d(TAG, "Error: " + anError.toString());
                            Log.d(TAG, "onError: " + anError.getErrorBody());
                            Log.d(TAG, "onError: " + anError.getErrorDetail());
                        }
                    });
        }
    }
}