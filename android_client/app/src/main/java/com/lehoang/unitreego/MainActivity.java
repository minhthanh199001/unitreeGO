package com.lehoang.unitreego;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.net.http.SslError;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.view.WindowManager;
import android.webkit.PermissionRequest;
import android.webkit.SslErrorHandler;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private static final String PREF_SERVER_IP = "server_ip";
    private static final int PERMISSION_REQUEST_CODE = 101;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Khóa màn hình luôn sáng trong lúc điều khiển robot
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hideSystemUI();

        prefs = getSharedPreferences("lehoang_robotics", Context.MODE_PRIVATE);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings ws = webView.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setDatabaseEnabled(true);
        ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(true);
        ws.setAllowContentAccess(true);
        ws.setUseWideViewPort(true);
        ws.setLoadWithOverviewMode(true);

        // Bỏ qua kiểm tra chứng chỉ SSL tự ký nội bộ (giải quyết triệt để cảnh báo bảo mật)
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
                handler.proceed(); // Chấp nhận cert nội bộ an toàn
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) {
                    showIpConfigDialog("Không thể kết nối tới máy chủ robot. Vui lòng kiểm tra IP và đảm bảo máy tính đang chạy server!");
                }
            }
        });

        // Tự động cấp quyền Micro cho Web Speech API để điều khiển giọng nói
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                request.grant(request.getResources());
            }
        });

        checkAndRequestPermissions();
        loadSavedServer();
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
            showIpConfigDialog("Chào mừng bạn! Vui lòng nhập địa chỉ IP máy tính đang chạy server:");
        } else {
            connectToServer(serverIp);
        }
    }

    private void connectToServer(String ip) {
        String url = ip.startsWith("http") ? ip : "https://" + ip;
        if (!url.contains(":") || url.lastIndexOf(":") < 6) {
            url += ":8080";
        }
        webView.loadUrl(url);
    }

    private void showIpConfigDialog(String message) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("🌐 CẤU HÌNH IP MÁY CHỦ ROBOT");
        builder.setMessage(message);

        final EditText input = new EditText(this);
        String currentIp = prefs.getString(PREF_SERVER_IP, "192.168.0.153:8080");
        input.setText(currentIp);
        builder.setView(input);

        builder.setPositiveButton("KẾT NỐI", (dialog, which) -> {
            String ip = input.getText().toString().trim();
            if (!ip.isEmpty()) {
                prefs.edit().putString(PREF_SERVER_IP, ip).apply();
                connectToServer(ip);
            }
        });

        builder.setCancelable(false);
        builder.show();
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            showIpConfigDialog("Bạn muốn đổi địa chỉ IP máy chủ kết nối?");
        }
    }
}
