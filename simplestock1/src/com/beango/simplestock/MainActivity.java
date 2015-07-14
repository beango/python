package com.beango.simplestock;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.beango.dal.DBHelper;
import com.beango.dal.MyStockDTO;
import com.beango.dal.MyStockExDTO;
import com.beango.util.HttpClients;
import com.beango.util.PersonAdapter;

import android.app.Activity;
import android.database.Cursor;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

public class MainActivity extends Activity {

	private ListView listView1;
	private ArrayList<MyStockDTO> data;
	private DBHelper dbHelper;
	private final static String DB_PATH = "/data/data/com.beango.simplestock/databases/";
	private final static String DB_NAME = "wlstock.s3db";
	private final static String pattern = "var hq_str_([a-z]*)([0-9]*)=\"(.*)\"";
	private Handler handler;
	private Handler handler2;
	private Runnable runnable;
	ArrayList<MyStockExDTO> framdata2 = new ArrayList<MyStockExDTO>();
	private PersonAdapter listadpter2;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		// 检查 SQLite 数据库文件是否存在
		if ((new File(DB_PATH + DB_NAME)).exists() == false) {
			// 如 SQLite 数据库文件不存在，再检查一下 database 目录是否存在
			File f = new File(DB_PATH);
			// 如 database 目录不存在，新建该目录
			if (!f.exists()) {
				f.mkdir();
			}
			try {
				// 得到 assets 目录下我们实现准备好的 SQLite 数据库作为输入流
				InputStream is = getBaseContext().getAssets().open(DB_NAME);
				// 输出流
				OutputStream os = new FileOutputStream(DB_PATH + DB_NAME);

				// 文件写入
				byte[] buffer = new byte[1024];
				int length;
				while ((length = is.read(buffer)) > 0) {
					os.write(buffer, 0, length);
				}

				// 关闭文件流
				os.flush();
				os.close();
				is.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		/*
		 * */
		findVidwByIds();
		fillData();
		listadpter2 = new PersonAdapter(this, framdata2);
		listView1.setAdapter(listadpter2);
		listView1.setOnItemClickListener(new OnItemClickListener() {
			/**
			 * parent当前所点击的listview对象 view当前所点击的条目
			 */
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

			}
		});

		// 用于定时刷新
		handler = new Handler();
		runnable = new Runnable() {
			@Override
			public void run() {
				fillData();
				handler.postDelayed(this, 3 * 1000);
			}
		};
		handler.postDelayed(runnable, 1000);
	}

	public void findVidwByIds() {
		listView1 = (ListView) findViewById(R.id.listView1);
	}

	public void fillData() {
		if (data == null)
			data = queryData();
		framdata2.clear();
		for (int i = 0; i < data.size(); i++) {
			MyStockDTO dto = data.get(i);
			MyStockExDTO dto2 = new MyStockExDTO();
			dto2.setStockno(dto.getStockno());
			dto2.setStocktype(dto.getStocktype());
			framdata2.add(dto2);
		}

		new Thread() {
			@Override
			public void run() {

				StringBuffer buf = new StringBuffer();
				for (MyStockDTO data : data) {
					buf.append(",").append(data.getStocktype() + data.getStockno());
				}

				if (buf.length() > 0) {
					HttpClients client = new HttpClients(MainActivity.this);
					String infos = client.doGet("http://hq.sinajs.cn/list=" + buf.substring(1));
					Message msg = new Message();
					msg.obj = infos;
					handler2.sendMessage(msg);
				}

			}
		}.start();
		// 定义Handler对象
		handler2 = new Handler() {
			@Override
			// 当有消息发送出来的时候就执行Handler的这个方法
			public void handleMessage(Message msg) {
				super.handleMessage(msg);
				// 处理UI
				handleMsg((String) msg.obj);
				Collections.reverse(framdata2);
				listadpter2.refresh(framdata2);
			}
		};
	}

	private void handleMsg(String infos) {
		String[] stockarr = infos.split("\n");

		for (String info : stockarr) {
			String stockno = "";
			String newprice = "";
			String stockname = "";
			String yesprice = "";
			Pattern r = Pattern.compile(pattern);
			Matcher m = r.matcher(info);

			if (m.find()) {
				stockno = m.group(2);
				String[] stockdata = m.group(3).split(",");
				newprice = stockdata[3];
				stockname = stockdata[0];
				yesprice = stockdata[2];
			} else {
				System.out.println("NO MATCH");
				continue;
			}

			MyStockExDTO d = null;
			for (MyStockExDTO d2 : framdata2) {
				if (d2.getStockno().equals(stockno)) {
					d = d2;
				}
			}

			if (null != d) {
				d.setNewprice(new Double(newprice));
				d.setStockname(stockname);

				double delay = new Double(newprice) - new Double(yesprice);
				double delayrate = delay * 100 / new Double(yesprice);
				delay = (double) (Math.round(delay * 100)) / 100;
				delayrate = (double) (Math.round(delayrate * 100)) / 100;
				d.setDelayprice(delay);
				d.setDelayrate(delayrate);
				if (new Double(newprice) == 0) {
					d.setDelayprice(0);
					d.setDelayrate(0);
				}
			}
		}
	}

	private Cursor queryData2() {
		dbHelper = new DBHelper(this);

		Cursor c = dbHelper.query();
		return c;
	}

	// 查询数据库，将每一行的数据封装成一个person 对象，然后将对象添加到List中
	private ArrayList<MyStockDTO> queryData() {
		ArrayList<MyStockDTO> list = new ArrayList<MyStockDTO>();
		dbHelper = new DBHelper(this);

		// 调用query()获取Cursor
		Cursor c = dbHelper.query();
		while (c.moveToNext()) {
			int _id = c.getInt(c.getColumnIndex("_id"));
			String stockno = c.getString(c.getColumnIndex("stockno"));
			String stocktype = c.getString(c.getColumnIndex("stocktype"));
			// 用一个Person对象来封装查询出来的数据
			MyStockDTO p = new MyStockDTO();
			p.setPkid(_id);
			p.setStockno(stockno);
			p.setStocktype(stocktype);

			list.add(p);
		}
		dbHelper.close();
		return list;
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	@Override
	protected void onDestroy() {
		// TODO Auto-generated method stub
		handler.removeCallbacks(runnable);// 停止定时器
		super.onDestroy();
	}

	@Override
	protected void onStop() {
		// TODO Auto-generated method stub
		handler.removeCallbacks(runnable);// 停止定时器
		super.onStop();
	}
}
