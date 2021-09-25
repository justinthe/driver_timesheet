package com.example.driver_management;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    private static String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d(TAG, "CP0");
    }

    public void navigateToApproval(View view) {
        Intent intent = new Intent(this, ApprovalActivity.class);
        startActivity(intent);
    }

    public void navigateToSummary(View view) {
        Intent intent = new Intent(this, SummaryActivity.class);
        startActivity(intent);
    }
}