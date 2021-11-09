//https://github.com/amitshekhariitbhu/Fast-Android-Networking

package com.example.driver_timesheet;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.JSONObjectRequestListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

    private static String TAG = "MAIN";
    Button button_in, button_out;
    String api_url;
    private Handler mainHandler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        api_url = getString(R.string.url_post_timesheet);
        button_in = (Button) findViewById(R.id.button_in);
        button_in.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                send_entry(true);
            }
        });

        button_out = (Button) findViewById(R.id.button_out);
        button_out.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                send_entry(false);
            }
        });

    }

    private void send_entry(boolean pInout) {
        boolean inout = false;
        if (pInout) {
            inout = true;
        }

        CreateEntry ce = new CreateEntry(inout, api_url);
        new Thread(ce).start();
    }

    class CreateEntry implements Runnable {

        Boolean inout;
        String api_url;

        CreateEntry(boolean inout, String api_url) {
            this.inout = inout;
            this.api_url = api_url;
        }

        @Override
        public void run() {
            JSONObject body = new JSONObject();
            SimpleDateFormat s = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String dt_now = s.format(new Date());
//            Log.d(TAG, "dt_now: " + dt_now);

            try {
                body.put("inout", inout);
                body.put("dttimeenter", dt_now);
            } catch (JSONException e) {
                Log.d(TAG, e.toString());
            }

            AndroidNetworking.post(api_url)
            .addJSONObjectBody(body)
            .setPriority(Priority.MEDIUM)
            .build()
            .getAsJSONObject(new JSONObjectRequestListener() {
                @Override
                public void onResponse(JSONObject response) {
                    Log.d(TAG, "Response: " + response);
                    Toast.makeText(getApplicationContext(), "Success", Toast.LENGTH_SHORT).show();
                }

                @Override
                public void onError(ANError anError) {
                    Log.d(TAG, "Error: " + anError);
                    Toast.makeText(getApplicationContext(), "Failed: " + anError.getMessage(), Toast.LENGTH_LONG).show();
                }
            });
        }


    }
}
