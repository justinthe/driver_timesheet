//https://github.com/amitshekhariitbhu/Fast-Android-Networking

package com.example.driver_timesheet;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
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

public class MainActivity extends AppCompatActivity {

    private static String TAG = "MAIN";
    Button button_in, button_out;
    String api_url;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        AndroidNetworking.initialize(getApplicationContext());

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

   private void send_entry(boolean pInout){
        boolean inout = false;
        if (pInout) {
            inout = true;
        }
        JSONObject body = new JSONObject();
        try {
            body.put("inout", inout);
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
                        Log.d(TAG, "Yay" + anError);
                        Toast.makeText(getApplicationContext(), "Success", Toast.LENGTH_SHORT).show();
                    }

                });
    }
}