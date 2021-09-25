package com.example.driver_management;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class ApprovalAdapter extends RecyclerView.Adapter<ApprovalAdapter.ApprovalViewHolder> {

    private static String TAG = "ApprovalAdapter";
    private ArrayList<Approval> dataList;

    public ApprovalAdapter(ArrayList<Approval> dataList) {
        this.dataList = dataList;
    }

    @NonNull
    @Override
    public ApprovalViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater layoutInflater = LayoutInflater.from(parent.getContext());
        View view = layoutInflater.inflate(R.layout.row_approval, parent, false);
        return new ApprovalViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ApprovalViewHolder holder, int position) {
        int pos = holder.getBindingAdapterPosition();
        holder.txtInout.setText(dataList.get(pos).getStr_inout());
        holder.txtDatetime.setText(dataList.get(pos).getStrDttimeenter());
        holder.cbApproval.setChecked(dataList.get(pos).isApproved());

        holder.cbApproval.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                dataList.get(pos).setApproved(b);
                Log.d(TAG, "timesheetid: " + b);
            }
        });
    }

    @Override
    public int getItemCount() {
        return (dataList != null) ? dataList.size() : 0;
    }


    public class ApprovalViewHolder extends RecyclerView.ViewHolder {
        private TextView txtDatetime, txtInout;
        private CheckBox cbApproval;

        public ApprovalViewHolder(View itemView) {
            super(itemView);
            cbApproval = (CheckBox) itemView.findViewById(R.id.cb_approval);
            txtDatetime = (TextView) itemView.findViewById(R.id.tv_datetime);
            txtInout = (TextView) itemView.findViewById(R.id.tv_inout);
        }
    }

}
