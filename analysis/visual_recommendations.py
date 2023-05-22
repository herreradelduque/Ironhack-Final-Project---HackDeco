# imports
import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def cos_simil(shop, product, img_features_user):
    shop_list = ["Ikea"]
    products_list = ["Sillas", "Sofás"]
    if shop in shop_list:
        if product in products_list:
            imgs_path = f"./data/img_{shop.lower()}_{product}/"
            imgs_path_arrange = f"../data/img_{shop.lower()}_{product}/"
            files = [imgs_path_arrange +
                     x for x in os.listdir(imgs_path) if "jpg" in x]
            # 5. compute cosine similarities
            imgs_features = np.load(
                f"./data/features_extraction_products/img_features_{shop}_{product}.npy"
            )
            # compute cosine similarities between images
            cos_similarities = cosine_similarity(
                imgs_features, img_features_user)
            cos_similarities = pd.DataFrame(cos_similarities)
            cos_similarities["Local_Path_cos"] = files
            furni_df = pd.read_csv(f"./data/{product}.csv")
            cos_similarities_merged_df = cos_similarities.merge(
                furni_df, left_on="Local_Path_cos", right_on="Local_Path"
            )
            cos_similarities_merged_df = cos_similarities_merged_df.sort_values(
                by=0, ascending=False
            )
            # Save json:
            cos_similarities_merged_df.to_json(
                f"./data/cos_similarities_{shop.lower()}_{product}.json",
                orient="records",
            )
        else:
            print("Selected product is not available")
    else:
        print("Selected shop is not available")
