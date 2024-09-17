from enum import Enum


class Queries(Enum):
    """
    An enum containing all GraphQL queries used by the client

    The attributes are named for the query they contain
    """
    MARATHONS = """
    query{
        marathons{
            id
            type
            type_id
            slug
            full_name
            total
            start_date
            stop_date
            playlist
            donationsTime{
                hour
                total
            }
            charity{
                id
                slug
                full_name
                website
                total
            }
            color
        }
    }"""

    MARATHON = """
    query($id: Int!){
        marathon(id: $id){
            id
            type
            type_id
            slug
            full_name
            total
            start_date
            stop_date
            playlist
            charity{
                id
                slug
                full_name
                website
                total
            }
            donationsTime{
                hour
                total
            }
            segments{
                id
                game{
                    id
                    title
                    iszelda
                    isevent
                }
                modifier
                raised
                start_time
                end_time
                vod
                time_offset
                runners{
                    attendee{
                        name
                        twitch_login
                        rank
                    }
                    rank
                }
                filenames{
                    filename
                    note
                }
            }
            attendance{
                attendee{
                    name
                    twitch_login
                    rank
                }
                award
                location
            }
            color
        }
    }"""

    GAMES = """
    query{
        games{
            id
            title
            iszelda
            isevent
        }
    }"""

    SEGMENTS = """
    query($method: String!, $id: Int!){
        segments(method: $method, id: $id){
            id
            game{
                id
                title
                iszelda
                isevent
            }
            modifier
            raised
            start_time
            end_time
            vod
            time_offset
            runners{
                attendee{
                    name
                    twitch_login
                    rank
                }
                rank
            }
            filenames{
                filename
                note
            }
        }
    }"""

    SOUNDS_DATA = """
    query{
        soundsdata{
            updated
            matching
            sounds{
                amount
                description
                verified
                newsound
                matched
            }
        }
    }"""

    ATTENDEES = """
    query{
        attendees{
            name
            twitch_login
            id
            rank
            house
            house_color
            segments{
                id
                game{
                    id
                    title
                    iszelda
                    isevent
                }
                modifier
                raised
                start_time
                end_time
                vod
                time_offset
                filenames{
                    filename
                    note
                }
            }
            attendance{
                marathon{
                    id
                    type
                    type_id
                    slug
                    full_name
                    total
                    start_date
                    stop_date
                    charity{
                        id
                        slug
                        full_name
                        website
                    }
                    color
                }
                award
                location
            }
        }
    }"""

    CHARITIES = """
    query{
        charities{
            id
            slug
            full_name
            website
            total
            marathons {
                full_name
                id
                slug
                start_date
                stop_date
                total
            }
        }
    }"""

    SOUND = """
    query($amount: Int!){
        sound(amount: $amount){
            amount
            description
            verified
            newsound
            matched
        }
    }"""

    SOUNDS = """
    query{
        sounds{
            amount
            description
            verified
            newsound
            matched
        }
    }"""
