def should_retrain(new_rmse, old_rmse, threshold=0.02):
    return new_rmse < old_rmse * (1 - threshold)
