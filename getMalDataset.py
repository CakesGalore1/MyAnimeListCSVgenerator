from mal import *
import math 
import csv




def get_anime(idValue):
    """
    Args: 
        int(Id): the MyAnimeList ID of the anime
    Return:
        Anime: the Anime object corrisponding to the id number
    """
    try:
        anime=Anime(idValue)
    except:
        ValueError: "idValue is not associated with an anime"
        return False
    else:
        return anime



def anime_to_data(idValue):
    """
    Args: 
        int(Id): the MyAnimeList ID of the anime
    Return:
        list: a list of various information about an anime according to MyAnimeList.net
    """
    anime = get_anime(idValue)
    if anime == False:
        return False
    data = [
anime.title,
anime.title_english,
anime.title_japanese,
anime.title_synonyms,
anime.url,
anime.image_url,
anime.type,
anime.status,
anime.genres,
anime.themes,
anime.score,
anime.scored_by,
anime.rank,
anime.popularity,
anime.members,
anime.favorites,
anime.episodes,
anime.aired,
anime.premiered,
anime.broadcast,
anime.producers,
anime.licensors,
anime.studios,
anime.source,
anime.duration,
anime.rating,
anime.related_anime,
anime.opening_themes,
anime.ending_themes,
anime.characters,
anime.staff,
anime.synopsis,
anime.background,
idValue]
    return data




def get_anime_dataset(minIndex = 1, maxIndex = 80000, progress_updates = True, progress_increment = .5):
    """
    
    """
    dataset =  []
    progress = 0
    for i in range(minIndex, maxIndex):
        current_data = anime_to_data(i)
        if current_data != False:
            dataset += [current_data]
            if progress_updates:
                if (i-minIndex)/(maxIndex-minIndex+1) > progress:
                    print("Progress: {0}%".format(progress*100))
                    progress += progress_increment
    return dataset


def make_csv(filename, minIndex, maxIndex, updates, progress_updates = True, progress_increment = .5):
    """
    
    """
    if maxIndex < minIndex:
        raise ValueError("maxIndex cannot be smaller than minIndex")
    if type(updates) != int:
        raise TypeError("updates must be an int")
    if updates <= 0:
        raise ValueError("updates must be greater or equal to 1")
    if (progress_increment < 0) or (progress_increment > 1):
        raise ValueError("progress_updates must be between 0 and 1")
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = "title","title_english","title_japanese","title_synonyms","url","image_url","type","status","genres","themes","score","scored_by","rank","popularity","members","favorites","episodes","aired","premiered","broadcast","producers","licensors","studios","source","duration","rating","related_anime","opening_themes","ending_themes","characters","staff","synopsis","background", "ID"
        writer.writerow(header)
        start = minIndex
        end = min(int((maxIndex-minIndex+1)/updates)+minIndex, maxIndex)
        for i in range(1, updates+1):
            print("start:",start)
            print("end:", end)
            writer.writerows(get_anime_dataset(start, end, progress_updates, progress_increment))
            start = max(minIndex, end)
            end = min(math.ceil((maxIndex-minIndex+1)/updates)+start, maxIndex)
        print("finished")
