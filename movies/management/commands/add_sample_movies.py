from django.core.management.base import BaseCommand
from django.core.files import File
from movies.models import Movie
from datetime import date
import os
from django.conf import settings
import shutil
import requests

class Command(BaseCommand):
    help = 'Adds sample movies with posters to the database'

    def handle(self, *args, **kwargs):
        # Create media directories if they don't exist
        media_root = settings.MEDIA_ROOT
        posters_dir = os.path.join(media_root, 'movie_posters')
        
        if not os.path.exists(media_root):
            os.makedirs(media_root)
        if not os.path.exists(posters_dir):
            os.makedirs(posters_dir)

        movies_data = [
            # Action Movies
            {
                'title': 'RRR',
                'director': 'S.S. Rajamouli',
                'cast': 'Ram Charan, N.T. Rama Rao Jr., Alia Bhatt',
                'description': 'A tale of two legendary revolutionaries and their journey far away from home.',
                'release_date': date(2022, 3, 24),
                'genre': 'Action',
                'language': 'Telugu',
                'duration': 182,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctODUxNy00ZTA2LWIyYTEtMDc5Y2E5ZjBmNTMzXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg'
            },
            # Comedy Movies
            {
                'title': 'Hera Pheri',
                'director': 'Priyadarshan',
                'cast': 'Akshay Kumar, Sunil Shetty, Paresh Rawal',
                'description': 'Three unemployed men find the answer to all their money problems when they receive a call from a kidnapper.',
                'release_date': date(2000, 3, 31),
                'genre': 'Comedy',
                'language': 'Hindi',
                'duration': 156,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDExMTBlZTYtZWMzYi00NmEwLWEzZGYtOTA1MDhmNTc0ODZkXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg'
            },
            # Drama Movies
            {
                'title': 'The Kerala Story',
                'director': 'Sudipto Sen',
                'cast': 'Adah Sharma, Yogita Bihani',
                'description': 'A coming-of-age drama about three girls from Kerala.',
                'release_date': date(2023, 5, 5),
                'genre': 'Drama',
                'language': 'Hindi',
                'duration': 138,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDA5YzlhNjItMDgxNC00NTViLTkxMzYtZWU3YjU3dTY2ZTI4XkEyXkFqcGdeQXVyMTU0ODI1NTA2._V1_.jpg'
            },
            # Romance Movies
            {
                'title': 'Sita Ramam',
                'director': 'Hanu Raghavapudi',
                'cast': 'Dulquer Salmaan, Mrunal Thakur',
                'description': 'An orphaned soldier\'s life changes after he receives a letter from a girl named Sita.',
                'release_date': date(2022, 8, 5),
                'genre': 'Romance',
                'language': 'Telugu',
                'duration': 163,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2RjZDJhYzUtOTQ5Yy00OWM3LWE5OTctYjRiYjU3ZGY5NzNkXkEyXkFqcGdeQXVyMTA3MDk2NDg2._V1_.jpg'
            },
            # Thriller Movies
            {
                'title': 'Drishyam 2',
                'director': 'Jeethu Joseph',
                'cast': 'Mohanlal, Meena, Ansiba Hassan',
                'description': 'A gripping tale of an investigation and a family threatened by it.',
                'release_date': date(2021, 2, 19),
                'genre': 'Thriller',
                'language': 'Malayalam',
                'duration': 152,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmY2ZDUxNzUtYWZlYy00MThhLWI5NjktZDhjZTU3MDY5YTM3XkEyXkFqcGdeQXVyMTA3MDk2NDg2._V1_.jpg'
            },
            # Horror Movies
            {
                'title': 'Tumbbad',
                'director': 'Rahi Anil Barve',
                'cast': 'Sohum Shah, Jyoti Malshe',
                'description': 'A mythological story about a goddess who created the entire universe.',
                'release_date': date(2018, 10, 12),
                'genre': 'Horror',
                'language': 'Hindi',
                'duration': 104,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmQxNmU4ZjgtYzE5Mi00ZDlhLTlhOTctMzJkNjk2ZGUyZGEwXkEyXkFqcGdeQXVyMzgxMDA0Nzk@._V1_.jpg'
            },
            # Fantasy Movies
            {
                'title': 'Ponniyin Selvan: I',
                'director': 'Mani Ratnam',
                'cast': 'Vikram, Aishwarya Rai Bachchan',
                'description': 'Vandiyathevan sets out to cross the Chola land to deliver a message from the Crown Prince Aditha Karikalan.',
                'release_date': date(2022, 9, 30),
                'genre': 'Fantasy',
                'language': 'Tamil',
                'duration': 167,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZjZlNGRhNTQtZTY1Yi00MTRlLWJhYjctYzdlZmYxNzEzYjNkXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg'
            },
            # Musical Movies
            {
                'title': 'Hridayam',
                'director': 'Vineeth Sreenivasan',
                'cast': 'Pranav Mohanlal, Kalyani Priyadarshan',
                'description': 'A coming-of-age romantic drama that follows the life of Arun from his college days.',
                'release_date': date(2022, 1, 21),
                'genre': 'Musical',
                'language': 'Malayalam',
                'duration': 172,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BOTc2ZTlmYmItMDBhYS00YmMzLWI4ZjAtMTI5YTBjOTFiMGEwXkEyXkFqcGdeQXVyMjkxNzQ1NDI@._V1_.jpg'
            },
            # Crime Movies
            {
                'title': 'Kaithi',
                'director': 'Lokesh Kanagaraj',
                'cast': 'Karthi, Narain, Arjun Das',
                'description': 'A prisoner on parole is forced to assist the police in a mission to stop a drug raid.',
                'release_date': date(2019, 10, 25),
                'genre': 'Crime',
                'language': 'Tamil',
                'duration': 145,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjMyNzQ3OTax._V1_.jpg'
            },
            # Add these to your movies_data list
            {
                'title': 'Animal',
                'director': 'Sandeep Reddy Vanga',
                'cast': 'Ranbir Kapoor, Rashmika Mandanna, Bobby Deol',
                'description': 'A son\'s love for his father becomes an obsession that unleashes a chain of violence.',
                'release_date': date(2023, 12, 1),
                'genre': 'Action',
                'language': 'Hindi',
                'duration': 201,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGViM2M4NmUtMmNkNy00MTQ5LTk5MDYtNmNhODAzODkwOTJlXkEyXkFqcGdeQXVyMTY1NDY4NTIw._V1_.jpg'
            },
            {
                'title': 'Dunki',
                'director': 'Rajkumar Hirani',
                'cast': 'Shah Rukh Khan, Taapsee Pannu',
                'description': 'A group of friends embark on an illegal journey to foreign lands in search of a better life.',
                'release_date': date(2023, 12, 21),
                'genre': 'Drama',
                'language': 'Hindi',
                'duration': 161,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMzQ0NDRhNmItYzllYS00NDdlLTk0YTctZjk5NzZhNTJhNTUyXkEyXkFqcGdeQXVyNTYwMzA0MTM@._V1_.jpg'
            },
            {
                'title': 'Salaar: Part 1 – Ceasefire',
                'director': 'Prashanth Neel',
                'cast': 'Prabhas, Prithviraj Sukumaran, Shruti Haasan',
                'description': 'A gang leader tries to keep a promise made to his dying friend.',
                'release_date': date(2023, 12, 22),
                'genre': 'Action',
                'language': 'Telugu',
                'duration': 175,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMmU2NzJkZWQtZmJhMC00YmU3LTk0MjktMTU3ZjRhZmM1NmIzXkEyXkFqcGdeQXVyMTUyNjIwMDEw._V1_.jpg'
            },
            {
                'title': 'Neru',
                'director': 'Jeethu Joseph',
                'cast': 'Mohanlal, Priya Mani, Anaswara Rajan',
                'description': 'A lawyer comes out of retirement to fight for justice.',
                'release_date': date(2023, 12, 21),
                'genre': 'Drama',
                'language': 'Malayalam',
                'duration': 145,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjBjM2RlYTctYTBhYi00VjE4LTg1ZTYtZjAyNzdhODVmOTQxXkEyXkFqcGdeQXVyMjkxNzQ1NDI@._V1_.jpg'
            },
            {
                'title': 'Hi Nanna',
                'director': 'Shouryuv',
                'cast': 'Nani, Mrunal Thakur',
                'description': 'A single father\'s life takes an unexpected turn when his past catches up with him.',
                'release_date': date(2023, 12, 7),
                'genre': 'Romance',
                'language': 'Telugu',
                'duration': 155,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BOTc5MmU2YDQ1ZWEtYjBiNi00ZGEwLTkwZDYtYzlmZDc2YTRiZDgwXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg'
            },
            {
                'title': 'Dhoomam',
                'director': 'Pawan Kumar',
                'cast': 'Fahadh Faasil, Aparna Balamurali',
                'description': 'A marketing professional\'s life turns upside down after a series of unusual events.',
                'release_date': date(2023, 6, 23),
                'genre': 'Thriller',
                'language': 'Malayalam',
                'duration': 150,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZTNhMjU2NTAtZTg5My00ZTg2LWIwZjMtNzRiNGFhZWQwOTZkXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg'
            },
            {
                'title': 'Maaveeran',
                'director': 'Madonne Ashwin',
                'cast': 'Sivakarthikeyan, Aditi Shankar',
                'description': 'A comic book artist gains the ability to hear his own character speak to him.',
                'release_date': date(2023, 7, 14),
                'genre': 'Action',
                'language': 'Tamil',
                'duration': 162,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZTllMjI3ZTQtZmZiYy00YmJiLWJiOTQtZWY0ZGUxNzE1NjY4XkEyXkFqcGdeQXVyMTUwMDg3OTQy._V1_.jpg'
            },
            {
                'title': 'Guthlee Ladoo',
                'director': 'Ishrat R. Khan',
                'cast': 'Sanjay Mishra, Dhanay Seth',
                'description': 'A Dalit boy dreams of going to school despite the social barriers.',
                'release_date': date(2023, 10, 13),
                'genre': 'Drama',
                'language': 'Hindi',
                'duration': 115,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjFiNTJmZjktMDk4YS00YWZhLWJiZmUtYzFhMjBhYzU0NDYyXkEyXkFqcGdeQXVyMTU4Mzg1OTU2._V1_.jpg'
            },
            {
                'title': 'Irugapatru',
                'director': 'Yuvaraj Dhayalan',
                'cast': 'Vikram Prabhu, Shraddha Srinath',
                'description': 'Three couples face different challenges in their relationships.',
                'release_date': date(2023, 11, 24),
                'genre': 'Romance',
                'language': 'Tamil',
                'duration': 145,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjBjZDM0YzctYTk3Yy00YjVhLWFhMTYtY2QxYTY3ZDQ5ZmRkXkEyXkFqcGdeQXVyMTU0ODI1NTA2._V1_.jpg'
            },
            {
                'title': 'Kaathal - The Core',
                'director': 'Jeo Baby',
                'cast': 'Mammootty, Jyothika',
                'description': 'A political leader\'s personal life becomes a subject of public scrutiny.',
                'release_date': date(2023, 11, 23),
                'genre': 'Drama',
                'language': 'Malayalam',
                'duration': 140,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZTc4YWY5MzAtOTc4Zi00NDVhLThlMDItYTI5NzNmYzdiOGU4XkEyXkFqcGdeQXVyMjkxNzQ1NDI@._V1_.jpg'
            },
            # Add these new movies to your movies_data list
            {
                'title': 'Napoleon',
                'director': 'Ridley Scott',
                'cast': 'Joaquin Phoenix, Vanessa Kirby',
                'description': 'An epic historical drama about Napoleon Bonaparte\'s rise to power.',
                'release_date': date(2023, 11, 22),
                'genre': 'Historical',
                'language': 'English',
                'duration': 158,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZWIzNDAxMTktMDMzZS00ZjJmLTlhNjYtOGUxYmZlZjMzZGU4XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_.jpg'
            },
            {
                'title': 'Tiger 3',
                'director': 'Maneesh Sharma',
                'cast': 'Salman Khan, Katrina Kaif',
                'description': 'Tiger embarks on a life-threatening mission to save his family and country.',
                'release_date': date(2023, 11, 12),
                'genre': 'Action',
                'language': 'Hindi',
                'duration': 155,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZGE5N2QyOGYtYjQ0Yy00MmU1LTk5Y2ItNGIwMjc2YjRiYWY3XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg'
            },
            {
                'title': 'Japan',
                'director': 'Raju Murugan',
                'cast': 'Karthi, Anu Emmanuel',
                'description': 'A mysterious man with a dark past seeks redemption.',
                'release_date': date(2023, 11, 10),
                'genre': 'Thriller',
                'language': 'Tamil',
                'duration': 152,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTNhNWRmODEtMzg5OS00ZTZkLWI3ODQtNDJiOGJmMGEyNGY1XkEyXkFqcGdeQXVyMTY3ODkyNDkz._V1_.jpg'
            },
            {
                'title': 'Mission Impossible: Dead Reckoning Part One',
                'director': 'Christopher McQuarrie',
                'cast': 'Tom Cruise, Hayley Atwell',
                'description': 'Ethan Hunt and his IMF team embark on their most dangerous mission yet.',
                'release_date': date(2023, 7, 12),
                'genre': 'Action',
                'language': 'English',
                'duration': 163,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYzFiZjc1YzctMDY3Zi00NGE5LTlmNWEtN2Q3OWFjYjY1NGM2XkEyXkFqcGdeQXVyMTUyMTUzNjQ0._V1_.jpg'
            },
            {
                'title': 'Oppenheimer',
                'director': 'Christopher Nolan',
                'cast': 'Cillian Murphy, Emily Blunt, Matt Damon',
                'description': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.',
                'release_date': date(2023, 7, 21),
                'genre': 'Biography',
                'language': 'English',
                'duration': 180,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_.jpg'
            },
            {
                'title': 'Barbie',
                'director': 'Greta Gerwig',
                'cast': 'Margot Robbie, Ryan Gosling',
                'description': 'Barbie and Ken go on a journey of self-discovery in the real world.',
                'release_date': date(2023, 7, 21),
                'genre': 'Comedy',
                'language': 'English',
                'duration': 114,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjU3N2QxNzYtMjk1NC00MTc4LTk1NTQtMmUxNTljM2I0NDA5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg'
            },
            {
                'title': 'Killers of the Flower Moon',
                'director': 'Martin Scorsese',
                'cast': 'Leonardo DiCaprio, Robert De Niro, Lily Gladstone',
                'description': 'Members of the Osage tribe in Oklahoma are murdered under mysterious circumstances in the 1920s.',
                'release_date': date(2023, 10, 20),
                'genre': 'Crime',
                'language': 'English',
                'duration': 206,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjE4ZTZlNDAtM2Q3YS00YjFhLThjN2UtODg2ZGNlN2E2MWU2XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_.jpg'
            },
            {
                'title': 'The Nun II',
                'director': 'Michael Chaves',
                'cast': 'Taissa Farmiga, Jonas Bloquet',
                'description': 'Sister Irene once again comes face to face with the demonic force Valak.',
                'release_date': date(2023, 9, 8),
                'genre': 'Horror',
                'language': 'English',
                'duration': 110,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BY2I4MDIwYWUtOWMxNC00ZTIzLWE3OGYtOWUyMmIwZGE2NjU4XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_.jpg'
            },
            {
                'title': 'Blue Beetle',
                'director': 'Angel Manuel Soto',
                'cast': 'Xolo Maridueña, Bruna Marquezine',
                'description': 'A Mexican-American teenager finds himself bonded to an alien scarab that gives him superpowered armor.',
                'release_date': date(2023, 8, 18),
                'genre': 'Superhero',
                'language': 'English',
                'duration': 127,
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMmY1ODUzZGItNDllOS00MDBhLTg4NmUtYjU4YjUxMGNlYmMwXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg'
            }
        ]

        for movie_data in movies_data:
            poster_url = movie_data.pop('poster_url')
            
            try:
                response = requests.get(poster_url, stream=True)
                if response.status_code == 200:
                    # Create a unique filename for the poster
                    poster_filename = f"{movie_data['title'].lower().replace(' ', '_')}_poster.jpg"
                    poster_path = os.path.join(posters_dir, poster_filename)
                    
                    # Save the poster image
                    with open(poster_path, 'wb') as f:
                        shutil.copyfileobj(response.raw, f)
                    
                    # Create or update movie with poster
                    movie, created = Movie.objects.get_or_create(
                        title=movie_data['title'],
                        defaults=movie_data
                    )
                    
                    # Update the poster field
                    with open(poster_path, 'rb') as f:
                        movie.poster.save(poster_filename, File(f), save=True)
                    
                    status = 'Created' if created else 'Updated'
                    self.stdout.write(
                        self.style.SUCCESS(f'{status} movie "{movie_data["title"]}" with poster')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error adding movie "{movie_data["title"]}": {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS('Successfully added all sample movies with posters'))