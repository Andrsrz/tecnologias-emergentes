package com.example.andrsrz.securitycamera.Activities;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobile.client.AWSStartupHandler;
import com.amazonaws.mobile.client.AWSStartupResult;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferListener;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferObserver;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferState;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferUtility;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.AmazonS3Exception;
import com.amazonaws.services.s3.model.ListObjectsRequest;
import com.amazonaws.services.s3.model.ListObjectsV2Request;
import com.amazonaws.services.s3.model.ListObjectsV2Result;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3ObjectSummary;
import com.example.andrsrz.securitycamera.R;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import Adapters.ImageAdapter;
import Classes.Image;

public class MainActivity extends AppCompatActivity {

    private static final String KEY = "AKIAJLVNYGRO4U45U3MQ";
    private static final String SECRET = "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";
    private static final String BUCKET_NAME = "securitycamera-userfiles-mobilehub-383062736";
    private static final int REQUEST = 1;

    private String fileName = "201806132033.jpg";
    private File localFolder = new File("sdcard/securitycamera");

    private List<Image> listImages;
    private List<Image> listImagesView;

    private ListView listView_ListImages;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        listView_ListImages = (ListView)findViewById(R.id.listView_ListImages);

        listImages = new ArrayList<>();
        listImagesView = new ArrayList<>();

        AWSMobileClient.getInstance().initialize(this, new AWSStartupHandler() {
            @Override
            public void onComplete(AWSStartupResult awsStartupResult) {
                Log.d("SecurityCamera", "AWSMobileClient is instantiated and you are connected to AWS!");
            }
        }).execute();

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
            SetPermissions();
            CreateFolder();
        }

        new LongOperation().execute("");
    }

    private void SetPermissions(){
        if ((ContextCompat.checkSelfPermission(this, android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED)
                && (ContextCompat.checkSelfPermission(this, android.Manifest.permission.READ_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED)) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE,android.Manifest.permission.READ_EXTERNAL_STORAGE},REQUEST);
        }
    }

    private void CreateFolder(){
        File folder = new File("sdcard/securitycamera");

        if (!folder.exists()){
            folder.mkdir();
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 1 && resultCode == RESULT_OK){
            CreateFolder();
        }
    }

    private File DownloadFile(AmazonS3 s3Client, final String BUCKET_NAME, String fileName, File localFolder){
        TransferUtility transferUtility =
                TransferUtility.builder()
                        .context(getApplicationContext())
                        .awsConfiguration(AWSMobileClient.getInstance().getConfiguration())
                        .s3Client(s3Client)
                        .build();

        File actualFile = new File(localFolder + "/" + fileName);
        TransferObserver downloadObserver = transferUtility.download(BUCKET_NAME, fileName, actualFile);

        downloadObserver.setTransferListener(new TransferListener() {
            @Override
            public void onStateChanged(int id, TransferState state) {
                if (TransferState.COMPLETED == state) {
                    // Handle a completed upload.
                }
            }

            @Override
            public void onProgressChanged(int id, long bytesCurrent, long bytesTotal) {
                float percentDonef = ((float)bytesCurrent/(float)bytesTotal) * 100;
                int percentDone = (int)percentDonef;
            }

            @Override
            public void onError(int id, Exception ex) {
                // Handle errors
            }
        });

        return actualFile;
    }

    private void SetView(){
        ImageAdapter myImageAdapter = new ImageAdapter(listImages, getApplicationContext());
        listView_ListImages.setAdapter(myImageAdapter);
        myImageAdapter.notifyDataSetChanged();
    }

    private class LongOperation extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            BasicAWSCredentials credentials = new BasicAWSCredentials(KEY, SECRET);
            AmazonS3 s3Client = new AmazonS3Client(credentials);
            ListObjectsV2Request listObjectsRequest = new ListObjectsV2Request();
            listObjectsRequest.setBucketName(BUCKET_NAME);

            ListObjectsV2Result result = s3Client.listObjectsV2(listObjectsRequest);

            for (S3ObjectSummary summary : result.getObjectSummaries()) {
                if (summary.getSize() > 0) {
                    Image AWSImage = new Image();
                    AWSImage.setFileName(summary.getKey());
                    AWSImage.setFile(DownloadFile(s3Client, BUCKET_NAME, summary.getKey(), localFolder));
                    SystemClock.sleep(3000);
                    listImages.add(AWSImage);
                }
            }

            return "Executed";
        }

        @Override
        protected void onPostExecute(String result) {
            if (result.equals("Executed")) {
                SetView();
            }
        }

        @Override
        protected void onPreExecute() {}

        @Override
        protected void onProgressUpdate(Void... values) {}
    }
}
