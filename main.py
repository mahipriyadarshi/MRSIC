import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from data import preprocess
from data.display import Main
st.set_page_config(layout="wide")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/744/744922.png", width=80)
    st.markdown("<h2 style='color:#22c55e;'>🎬 Movie Recommender</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color:#cbd5e1;'>Built using TMDB API & ML</span>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #22c55e;'>", unsafe_allow_html=True)
    st.markdown("<span style='color:#a3e635;'>Made by Priyadarshi Mahi ❤️</span>", unsafe_allow_html=True)


# Setting the wide mode as default
st.markdown("<h1 style='text-align: center; color: teal;'>Movie Recommender 🎥</h1>", unsafe_allow_html=True)


displayed = []

if 'movie_number' not in st.session_state:
    st.session_state['movie_number'] = 0

if 'selected_movie_name' not in st.session_state:
    st.session_state['selected_movie_name'] = ""

if 'user_menu' not in st.session_state:
    st.session_state['user_menu'] = ""


def main():
    def apply_custom_css():
        st.markdown("""
        <style>
        .css-1d391kg ul {
        background-color: white !important;
        border-radius: 10px;
        padding: 0.5rem;
    }

    /* Inactive menu item */
    .css-1d391kg ul li a {
        color: teal !important;
        background-color: #e0f7f7 !important;
        border-radius: 10px;
    }

    /* Active (selected) menu item */
    .css-1d391kg ul li.active a {
        background-color: teal !important;
        color: white !important;
        border-radius: 10px;
    }

    /* Hover effect */
    .css-1d391kg ul li a:hover {
        background-color: #b2dfdb !important;
        color: black !important;
    }
        
            div[role="tablist"] > div[aria-selected="true"] {
            background-color: teal !important;
            color: white !important;
            border-radius: 5px;
        }

        /* Style for inactive (unselected) options */
        div[role="tablist"] > div {
            color: teal !important;
            background-color: #e0f7f7 !important;
            border-radius: 5px;
        }

        /* Add hover effect */
        div[role="tablist"] > div:hover {
            background-color: #b2dfdb !important;
            color: black !important;
        }
        .movie-card {
            border-radius: 12px;
            padding: 10px;
            background-color: #1a1a1a;
            color: #22c55e;
            box-shadow: 0 4px 14px rgba(34, 197, 94, 0.25);
            transition: transform 0.2s;
            text-align: center;
        }
        .movie-card:hover {
            transform: scale(1.05);
            background-color: #111;
        }
        .movie-title {
            font-weight: bold;
            color: #86efac;
        }
        .recommend-header {
            color: #bbf7d0;
            font-size: 20px;
            margin-bottom: 5px;
        }
        .stButton>button {
            background-color: #22c55e;
            color: black;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #16a34a;
            color: white;
        }
        .stSelectbox > div > div {
            color: #22c55e;
        }
        .stSlider > div > div > div {
            background-color: #22c55e;
        }
        .st-bb {
            color: #22c55e;
        }
        h1, h2, h3, h4 {
            color: #22c55e;
        }
        </style>
        """, unsafe_allow_html=True)

    apply_custom_css()
    def initial_options():
        # To display menu
        

        st.session_state.user_menu = streamlit_option_menu.option_menu(
            menu_title='What are you looking for? 👀',
            options=['Recommend me a similar movie', 'Describe me a movie', 'Check all Movies'],
            icons=['film', 'film', 'film'],
            menu_icon='list',
            orientation="horizontal",
        )

        if st.session_state.user_menu == 'Recommend me a similar movie':
            recommend_display()

        elif st.session_state.user_menu == 'Describe me a movie':
            display_movie_details()

        elif st.session_state.user_menu == 'Check all Movies':
            paging_movies()

    def recommend_display():

        st.title('Movie Recommender System')

        selected_movie_name = st.selectbox(
            'Select a Movie...', new_df['title'].values
        )

        rec_button = st.button('Recommend')
        if rec_button:
            st.session_state.selected_movie_name = selected_movie_name
            recommendation_tags(new_df, selected_movie_name, r'models/similarity_tags_tags.pkl',"are")
            recommendation_tags(new_df, selected_movie_name, r'models/similarity_tags_genres.pkl',"on the basis of genres are")
            recommendation_tags(new_df, selected_movie_name,
                                r'models/similarity_tags_tprduction_comp.pkl',"from the same production company are")
            recommendation_tags(new_df, selected_movie_name, r'models/similarity_tags_keywords.pkl',"on the basis of keywords are")
            recommendation_tags(new_df, selected_movie_name, r'models/similarity_tags_tcast.pkl',"on the basis of cast are")

    def recommendation_tags(new_df, selected_movie_name, pickle_file_path,str):

        movies, posters = preprocess.recommend(new_df, selected_movie_name, pickle_file_path)
        st.subheader(f'Best Recommendations {str}...')

        rec_movies = []
        rec_posters = []
        cnt = 0
        # Adding only 5 uniques recommendations
        for i, j in enumerate(movies):
            if cnt == 5:
                break
            if j not in displayed:
                rec_movies.append(j)
                rec_posters.append(posters[i])
                displayed.append(j)
                cnt += 1

        # Columns to display informations of movies i.e. movie title and movie poster
        cols = st.columns(5)
        for i in range(len(rec_movies)):
            with cols[i]:
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{rec_posters[i]}" width="100%">
                    <div class="movie-title">{rec_movies[i]}</div>
                </div>
                """, unsafe_allow_html=True)


    def display_movie_details():

        selected_movie_name = st.session_state.selected_movie_name
        movie_id = movies[movies['title'] == selected_movie_name]['movie_id']
        info = preprocess.get_details(selected_movie_name)

        with st.container():
            image_col, text_col = st.columns((1, 2))
            with image_col:
                st.text('\n')
                st.image(info[0])

            with text_col:
                st.text('\n')
                st.text('\n')
                st.title(selected_movie_name)
                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Rating")
                    st.write(info[8])
                with col2:
                    st.text("No. of ratings")
                    st.write(info[9])
                with col3:
                    st.text("Runtime")
                    st.write(info[6])

                st.text('\n')
                st.write("Overview")
                st.write(info[3], wrapText=False)
                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Release Date")
                    st.text(info[4])
                with col2:
                    st.text("Budget")
                    st.text(info[1])
                with col3:
                    st.text("Revenue")
                    st.text(info[5])

                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    str = ""
                    st.text("Genres")
                    for i in info[2]:
                        str = str + i + " . "
                    st.write(str)

                with col2:
                    str = ""
                    st.text("Available in")
                    for i in info[13]:
                        str = str + i + " . "
                    st.write(str)
                with col3:
                    st.text("Directed by")
                    st.text(info[12][0])
                st.text('\n')


        # Displaying information of casts.
        st.header('Cast')
        cnt = 0
        urls = []
        bio = []
        for i in info[14]:
            if cnt == 5:
                break
            url, biography= preprocess.fetch_person_details(i)
            urls.append(url)
            bio.append(biography)
            cnt += 1

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(urls[0])
            # Toggle button to show information of cast.
            stoggle(
                "Show More",
                bio[0],
            )
        with col2:
            st.image(urls[1])
            stoggle(
                "Show More",
                bio[1],
            )
        with col3:
            st.image(urls[2])
            stoggle(
                "Show More",
                bio[2],
            )
        with col4:
            st.image(urls[3])
            stoggle(
                "Show More",
                bio[3],
            )
        with col5:
            st.image(urls[4])
            stoggle(
                "Show More",
                bio[4],
            )

    def paging_movies():
        # To create pages functionality using session state.
        max_pages = movies.shape[0] / 10
        max_pages = int(max_pages) - 1

        col1, col2, col3 = st.columns([1, 9, 1])

        with col1:
            st.text("Previous page")
            prev_btn = st.button("Prev")
            if prev_btn:
                if st.session_state['movie_number'] >= 10:
                    st.session_state['movie_number'] -= 10

        with col2:
            new_page_number = st.slider("Jump to page number", 0, max_pages, st.session_state['movie_number'] // 10)
            st.session_state['movie_number'] = new_page_number * 10

        with col3:
            st.text("Next page")
            next_btn = st.button("Next")
            if next_btn:
                if st.session_state['movie_number'] + 10 < len(movies):
                    st.session_state['movie_number'] += 10

        display_all_movies(st.session_state['movie_number'])

    def display_all_movies(start):

        i = start
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        st.session_state['page_number'] = i

    with Main() as bot:
        bot.main_()
        new_df, movies, movies2 = bot.getter()
        initial_options()


if __name__ == '__main__':
    main()
