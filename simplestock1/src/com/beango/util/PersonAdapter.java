package com.beango.util;

import java.util.ArrayList;

import com.beango.dal.MyStockExDTO;
import com.beango.simplestock.R;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

public class PersonAdapter extends BaseAdapter {
	private ArrayList<MyStockExDTO> mList;
	private Context mContext;

	public PersonAdapter(Context context, ArrayList<MyStockExDTO> list) {
		mList = list;
		mContext = context;
	}

	public void refresh(ArrayList<MyStockExDTO> list) {
		mList = list;
		notifyDataSetChanged();
	}

	@Override
	public int getCount() {
		return mList.size();
	}

	@Override
	public Object getItem(int position) {
		return mList.get(position);
	}

	@Override
	public long getItemId(int position) {
		return position;
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {

		Holder holder = null;
		if (convertView == null) {
			LayoutInflater inflater = LayoutInflater.from(mContext);
			convertView = inflater.inflate(R.layout.item, null);
			holder = new Holder();
			holder.mNameText = (TextView) convertView.findViewById(R.id.stockname);
			holder.mNoText = (TextView) convertView.findViewById(R.id.stockno);
			holder.mNewPriceText = (TextView) convertView.findViewById(R.id.newprice);
			holder.mDelayText = (TextView) convertView.findViewById(R.id.delayprice);
			holder.mDelayRateText = (TextView) convertView.findViewById(R.id.delayrate);
			convertView.setTag(holder);
		} else {
			holder = (Holder) convertView.getTag();
		}
		double newprice = mList.get(getCount() - position - 1).getNewprice();
		double delayprice = mList.get(getCount() - position - 1).getDelayprice();
		holder.mNameText.setText(mList.get(getCount() - position - 1).getStockname());
		holder.mNoText.setText(mList.get(getCount() - position - 1).getStockno());
		if (newprice != 0) {
			holder.mNewPriceText.setText(Double.toString(newprice));
			holder.mDelayText.setText(Double.toString(delayprice));
			holder.mDelayRateText.setText(Double.toString(mList.get(getCount() - position - 1).getDelayrate()) + "%");
		}
		if(delayprice>0)
		{
			holder.mDelayText.setTextColor(Color.RED);
			holder.mDelayRateText.setTextColor(Color.RED);
		}
		if(delayprice<0)
		{
			holder.mDelayText.setTextColor(Color.GREEN);
			holder.mDelayRateText.setTextColor(Color.GREEN);
		}
		return convertView;
	}

	class Holder {
		private TextView mNameText, mNoText, mNewPriceText, mDelayText, mDelayRateText;
	}
}
