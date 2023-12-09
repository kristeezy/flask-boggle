from flask import Flask, redirect, render_template, flash

# ... (existing code)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist_detail.html", playlist=playlist)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:
    
    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    
    form = PlaylistForm()
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        new_playlist = Playlist(name=name, description=description)
        db.session.add(new_playlist)
        db.session.commit()

        flash('Playlist created successfully!', 'success')
        return redirect("/playlists")

    return render_template("add_playlist.html", form=form)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data

        new_song = Song(title=title, artist=artist)
        db.session.add(new_song)
        db.session.commit()

        flash('Song created successfully!', 'success')
        return redirect("/songs")

    return render_template("add_song.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""
    
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()
    
    # Get the songs not already on this playlist
    curr_on_playlist = [song.id for song in playlist.songs]
    form.song.choices = [(song.id, f'{song.title} - {song.artist}') for song in Song.query.filter(Song.id.notin_(curr_on_playlist))]
    
    if form.validate_on_submit():
        song_id = form.song.data
        song = Song.query.get(song_id)
        
        playlist.songs.append(song)
        db.session.commit()
        
        flash(f'Song "{song.title}" added to playlist "{playlist.name}" successfully!', 'success')
        return redirect(f"/playlists/{playlist_id}")
    
    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)
