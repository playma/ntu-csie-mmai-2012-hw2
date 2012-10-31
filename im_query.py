
    # traverse the target_dir, build color vector file for *.jpg in target_dir
    for root,dirs,files in os.walk(target_dir):
        for filename in files:
            # check the file is a jpeg file
            if filename.split('.')[-1].lower() in ['jpg','jpeg']:

                # image filename
                target_image = os.path.join(root,filename)
                
                # cache filename



