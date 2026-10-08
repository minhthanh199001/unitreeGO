package com.lehoang.unitreego;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.http.SslError;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.SslErrorHandler;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private static final String PREF_SERVER_IP = "server_ip";
    private static final String PREF_HISTORY_IPS = "history_ips";
    private static final int PERMISSION_REQUEST_CODE = 101;
    private static final String DEFAULT_IP = "192.168.0.60:8080";

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Khóa màn hình luôn sáng trong lúc điều khiển robot
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hideSystemUI();

        prefs = getSharedPreferences("lehoang_robotics", Context.MODE_PRIVATE);

        // Tạo FrameLayout chứa WebView và nút nổi ⚙️ IP Server
        FrameLayout rootLayout = new FrameLayout(this);
        rootLayout.setBackgroundColor(Color.parseColor("#080B12"));

        webView = new WebView(this);
        rootLayout.addView(webView, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT
        ));

        // Nút nổi nhỏ góc trên bên phải để người dùng mở cấu hình IP Server bất cứ lúc nào
        Button btnIpConfig = new Button(this);
        btnIpConfig.setText("⚙️ IP");
        btnIpConfig.setTextSize(11);
        btnIpConfig.setTextColor(Color.parseColor("#00F0FF"));
        btnIpConfig.setAlpha(0.70f);

        GradientDrawable btnBg = new GradientDrawable();
        btnBg.setColor(Color.parseColor("#990F172A"));
        btnBg.setStroke(2, Color.parseColor("#00F0FF"));
        btnBg.setCornerRadius(14);
        btnIpConfig.setBackground(btnBg);

        FrameLayout.LayoutParams btnParams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT,
                FrameLayout.LayoutParams.WRAP_CONTENT
        );
        btnParams.gravity = Gravity.TOP | Gravity.END;
        btnParams.topMargin = 16;
        btnParams.rightMargin = 16;
        btnIpConfig.setLayoutParams(btnParams);
        btnIpConfig.setPadding(20, 8, 20, 8);

        btnIpConfig.setOnClickListener(v -> showIpConfigDialog("Cấu hình địa chỉ IP máy chủ kết nối"));
        rootLayout.addView(btnIpConfig);

        setContentView(rootLayout);

        // Cấu hình WebView
        WebSettings ws = webView.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setDatabaseEnabled(true);
        ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(true);
        ws.setAllowContentAccess(true);
        ws.setUseWideViewPort(true);
        ws.setLoadWithOverviewMode(true);

        // Tích hợp cầu nối Javascript gọi từ giao diện Web
        webView.addJavascriptInterface(new WebAppInterface(this), "AndroidApp");

        // Bỏ qua kiểm tra chứng chỉ SSL tự ký nội bộ (tránh cảnh báo đỏ)
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
                handler.proceed();
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) {
                    showIpConfigDialog("Không thể kết nối tới máy chủ tại: " + getCurrentServerIp() + "\nVui lòng kiểm tra lại IP hoặc đảm bảo máy tính đang chạy 2_CHAY_ROBOT.bat!");
                }
            }
        });

        // Tự động cấp quyền Micro cho Web Speech API
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                request.grant(request.getResources());
            }
        });

        checkAndRequestPermissions();
        loadSavedServer();
    }

    public class WebAppInterface {
        Context mContext;

        WebAppInterface(Context c) {
            mContext = c;
        }

        @JavascriptInterface
        public void openServerSettings() {
            runOnUiThread(() -> showIpConfigDialog("Cấu hình địa chỉ IP máy chủ kết nối"));
        }

        @JavascriptInterface
        public String getCurrentServerIp() {
            return MainActivity.this.getCurrentServerIp();
        }
    }

    private String getCurrentServerIp() {
        return prefs.getString(PREF_SERVER_IP, DEFAULT_IP);
    }

    private void hideSystemUI() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            final WindowInsetsController insetsController = getWindow().getInsetsController();
            if (insetsController != null) {
                insetsController.hide(WindowInsets.Type.statusBars() | WindowInsets.Type.navigationBars());
                insetsController.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
            }
        } else {
            getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_FULLSCREEN
            );
        }
    }

    private void checkAndRequestPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, PERMISSION_REQUEST_CODE);
        }
    }

    private void loadSavedServer() {
        String serverIp = prefs.getString(PREF_SERVER_IP, "");
        if (serverIp.isEmpty()) {
            showIpConfigDialog("Chào mừng bạn! Vui lòng chọn hoặc nhập địa chỉ IP máy tính đang chạy server:");
        } else {
            connectToServer(serverIp);
        }
    }

    private void connectToServer(String ip) {
        String cleanIp = ip.trim();
        if (!cleanIp.contains(":") || cleanIp.lastIndexOf(":") < 6) {
            cleanIp += ":8080";
        }
        prefs.edit().putString(PREF_SERVER_IP, cleanIp).apply();
        saveToHistory(cleanIp);

        String url = cleanIp.startsWith("http") ? cleanIp : "https://" + cleanIp;
        webView.loadUrl(url);
    }

    private void saveToHistory(String ip) {
        Set<String> history = new HashSet<>(prefs.getStringSet(PREF_HISTORY_IPS, new HashSet<>()));
        history.add(ip);
        prefs.edit().putStringSet(PREF_HISTORY_IPS, history).apply();
    }

    public void showIpConfigDialog(String message) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("🌐 CHỌN ĐỊA CHỈ IP SERVER");

        ScrollView scrollView = new ScrollView(this);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(40, 25, 40, 20);

        TextView tvMsg = new TextView(this);
        tvMsg.setText(message);
        tvMsg.setTextSize(13);
        tvMsg.setTextColor(Color.parseColor("#94A3B8"));
        layout.addView(tvMsg);

        // Ô nhập IP thủ công
        TextView tvLabel = new TextView(this);
        tvLabel.setText("Nhập IP máy tính (Cổng mặc định: 8080):");
        tvLabel.setTextSize(13);
        tvLabel.setTypeface(null, Typeface.BOLD);
        tvLabel.setTextColor(Color.WHITE);
        tvLabel.setPadding(0, 25, 0, 10);
        layout.addView(tvLabel);

        final EditText input = new EditText(this);
        String currentIp = getCurrentServerIp();
        input.setText(currentIp);
        input.setSingleLine(true);
        input.setTextColor(Color.WHITE);
        input.setHint("VD: 192.168.0.60:8080");
        input.setHintTextColor(Color.parseColor("#64748B"));
        layout.addView(input);

        // Danh sách gợi ý chọn nhanh
        TextView tvPresets = new TextView(this);
        tvPresets.setText("Gợi ý chọn nhanh (Chạm để chọn):");
        tvPresets.setTextSize(12);
        tvPresets.setTextColor(Color.parseColor("#00F0FF"));
        tvPresets.setPadding(0, 30, 0, 10);
        layout.addView(tvPresets);

        List<String> presetList = new ArrayList<>(Arrays.asList(
                "192.168.0.60:8080",
                "192.168.0.153:8080",
                "192.168.0.41:8080",
                "192.168.12.1:8080",
                "localhost:8080"
        ));

        Set<String> history = prefs.getStringSet(PREF_HISTORY_IPS, new HashSet<>());
        for (String histIp : history) {
            if (!presetList.contains(histIp)) {
                presetList.add(0, histIp);
            }
        }

        LinearLayout presetsContainer = new LinearLayout(this);
        presetsContainer.setOrientation(LinearLayout.VERTICAL);

        for (String preset : presetList) {
            Button btnPreset = new Button(this);
            btnPreset.setText("🔗 " + preset);
            btnPreset.setTextSize(12);
            btnPreset.setTextColor(Color.parseColor("#E2E8F0"));
            btnPreset.setGravity(Gravity.START | Gravity.CENTER_VERTICAL);
            btnPreset.setBackgroundColor(Color.TRANSPARENT);
            btnPreset.setPadding(10, 10, 10, 10);
            btnPreset.setOnClickListener(v -> input.setText(preset));
            presetsContainer.addView(btnPreset);
        }
        layout.addView(presetsContainer);

        scrollView.addView(layout);
        builder.setView(scrollView);

        builder.setPositiveButton("KẾT NỐI", (dialog, which) -> {
            String ip = input.getText().toString().trim();
            if (!ip.isEmpty()) {
                connectToServer(ip);
                Toast.makeText(MainActivity.this, "Đang kết nối tới: " + ip, Toast.LENGTH_SHORT).show();
            }
        });

        builder.setNegativeButton("ĐÓNG", (dialog, which) -> dialog.dismiss());

        AlertDialog dialog = builder.create();
        dialog.show();
    }

    @Override
    public void onBackPressed() {
        showIpConfigDialog("Bạn muốn thay đổi địa chỉ IP Server hay tải lại trang?");
    }
}
