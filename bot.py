from aiogram import executor
from create_bot import dp
from heandlers import creator, worker, user


if __name__ == "__main__":
    creator.heandlerCreator(dp)
    worker.heandlersWorker(dp)
    user.heandlersClient(dp)
    executor.start_polling(dp, skip_updates=True)