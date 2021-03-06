import requests
from bs4 import BeautifulSoup
import re


def find_articles(desired_hubs):
    output_list = []

    # получаем страницу с самыми свежими постами
    ret_1 = requests.get('https://habr.com/ru')
    soup_1 = BeautifulSoup(ret_1.text, 'html.parser')

    # извлекаем посты
    posts = soup_1.find_all('article', class_='post')
    for post in posts:
        # находим дату и время выпуска поста
        date = post.find('span', class_='post__time')
        hubs = post.find_all('a', class_='hub-link')
        post_title = post.find('a', class_='post__title_link')
        post_title_lower = post_title.text.lower()
        words_list_post_title_lower = post_title_lower.split(' ')
        preview_text = post.find('div', class_='post__text')
        preview_text_lower = preview_text.text.lower()
        words_preview_text_list_lower = preview_text_lower.split(' ')
        # ищем ключевые слова в названии поста
        for one_word in words_list_post_title_lower:
            if any([one_word in desired_hubs]):
                output_list.append(f"{date.text} - {post_title.text} - {post_title.attrs.get('href')}")
                break
        # ищем ключевые слова в хабах поста
        for hub in hubs:
            hub_lower = hub.text.lower()
            if any([hub_lower in desired_hubs]):
                article = f"{date.text} - {post_title.text} - {post_title.attrs.get('href')}"
                if article not in output_list:
                    output_list.append(article)
                break
        # ищем ключевые слова в превью поста
        for word in words_preview_text_list_lower:
            if any([word in desired_hubs]):
                article_name = f"{date.text} - {post_title.text} - {post_title.attrs.get('href')}"
                if article_name not in output_list:
                    output_list.append(article_name)
                break

        # ищем ключевые слова в полной версии поста
        str_of_this_article = f"{date.text} - {post_title.text} - {post_title.attrs.get('href')}"
        if str_of_this_article not in output_list:
            ret_2 = requests.get(post_title.attrs.get('href'))
            soup_2 = BeautifulSoup(ret_2.text, 'html.parser')
            article_texts = soup_2.find_all('div', class_='post__text')
            for one_text in article_texts:
                one_text_lower = one_text.text.lower()
                words_article_text_lower = one_text_lower.split(' ')
                for one_part in words_article_text_lower:
                    one_part = re.sub(r"[,]", "", one_part)
                    if any([one_part in desired_hubs]):
                        output_list.append(str_of_this_article)
                        break

    # печатаем список подошедших постов
    for one_article in output_list:
        print(one_article)


if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    find_articles(KEYWORDS)

