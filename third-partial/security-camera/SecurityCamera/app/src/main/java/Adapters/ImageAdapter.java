package Adapters;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.annotation.NonNull;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.example.andrsrz.securitycamera.R;
import com.squareup.picasso.Picasso;

import java.io.File;
import java.util.List;

import Classes.Image;

public class ImageAdapter extends ArrayAdapter<Image>{
    List<Image> imagesList;
    Context myContext;

    public ImageAdapter(List<Image> imagesList, Context myContext){
        super(myContext, R.layout.list_items, imagesList);
        this.imagesList = imagesList;
        this.myContext = myContext;
    }

    @Override
    public View getView(int position, View convertView, @NonNull ViewGroup parent){
        LayoutInflater inflater = LayoutInflater.from(myContext);
        View listViewItem = inflater.inflate(R.layout.list_items, null, true);
        ImageView imageView_background = listViewItem.findViewById(R.id.imageView_ListItems);
        TextView textView_Service = listViewItem.findViewById(R.id.textView_ListItems);
        Image items = imagesList.get(position);
        textView_Service.setText("Master, someone is in your bedroom.\n" + items.getFileName());
        File imgFile = items.getFile();
        Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getPath());
        imageView_background.setImageBitmap(myBitmap);

        return listViewItem;
    }
}
