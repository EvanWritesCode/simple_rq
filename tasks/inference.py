## Taken from bxingest/imagetagger.py egate inference

# if MODEL_DIR:

#         model_path = pathlib.Path(MODEL_DIR)
#         print("Model path: {}".format(model_path))

#         print("Fetching and preparing images for inference...")
#         img_desc_list = prep_images_for_inference(images)
#         print("Fetch and prepare images complete.")

#         # EGATE MODEL
#         egate_model_path = model_path / "egate_model"
#         print("Using custom tagger for tag: '{}'".format(EG_CUSTOM_TAG))
#         eg = Egate(model_dir=egate_model_path)
#         is_egates, failed_images = eg.is_egate2(img_desc_list)

#         for img_id in is_egates.keys():
#             # Results are returned always sorted
#             _category, _confidence = is_egates[img_id][0]
#             tag = [(EG_CUSTOM_TAG, _confidence)] if "egate" in _category else []
#             if img_id in results:
#                 results[img_id]["custom"] = tag
#             else:
# results[img_id] = {"custom": tag}