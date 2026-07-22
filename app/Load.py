from app.Database.Repository import CryptoRepository


def load_data(df):

    CryptoRepository.save_dataframe(df)

    print(f"{len(df)} records inserted successfully.")


def remove_old_data():

    CryptoRepository.remove_old_data()