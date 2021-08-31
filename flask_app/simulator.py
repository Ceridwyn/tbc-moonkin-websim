from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .encounter import Encounter
from .buffs_list import Buffs_list
from .character import Character

bp = Blueprint('simulator', __name__)

@bp.route('/')
def index():
    return render_template('simulator/index.html')

@bp.route('/formtest', methods=('GET', 'POST'))
def form_test():
    intel = request.form['intel']
    sp = request.form['sp']
    return render_template('simulator/test_form.html', intellect=intel, spellpower=sp)

@bp.route('/simulate', methods=('GET', 'POST'))
def simulate_fight():
    # Concernant les checkbox, quand une est decochee le parametre ne sera pas present dans le POST
    if request.method == 'POST':
        # Character creation from posted arguments
        toon = Character(
        intel = int(request.form['intel']),
        spellpower = int(request.form['spellpower']),
        hit_score = int(request.form['spell_hit']),
        crit_score = int(request.form['spell_crit']),
        haste = int(request.form['spell_haste']),
        spirit = int(request.form['spirit']),
        trinket1 = request.form['trinket1'],
        trinket2 = request.form['trinket2'],
        idol = request.form['idol'],
        is_csd = 'is_csd' in request.form,
        is_spellstrike = 'is_spellstrike' in request.form,
        is_spellfire = 'is_spellstrike' in request.form)
        toon.set_talents(
        balance_of_power = "balance_of_power" in request.form,
        focused_starlight = "focused_starlight" in request.form,
        moonkin_form = "moonkin_form" in request.form,
        improved_mf = "improved_mf" in request.form,
        starlight_wrath = "starlight_wrath" in request.form,
        vengeance = "vengeance" in request.form,
        lunar_guidance = "lunar_guidance" in request.form,
        moonfury = "moonfury" in request.form,
        wrath_of_cenarius = "wrath_of_cenarius" in request.form)        
        
        # Buffs from posted arguments
        if "is_curse_of_elements" in request.form :
            if "is_improved_coe" in request.form :
                curse_of_elements = 1.13
            else :
                curse_of_elements = 1.1
        else:
            curse_of_elements = 1
        buffs = Buffs_list(
        is_motw = 'is_motw' in request.form,
        is_totem_of_wrath = "is_totem_of_wrath" in request.form,
        is_divine_spirit = "is_divine_spirit" in request.form,
        is_arcane_brilliance = "is_arcane_brilliance" in request.form,
        is_wrath_of_air = "is_wrath_of_air" in request.form,
        is_draenei_in_group = "is_draenei_in_group" in request.form,
        curse_of_elements = curse_of_elements,
        is_blessing_kings = "is_blessing_kings" in request.form,
        is_crusader = "is_crusader" in request.form,
        is_sham_4_piece = "is_sham_4_piece" in request.form,
        is_flask = "is_flask" in request.form,
        is_food = "is_food" in request.form,
        is_oil = "is_oil" in request.form,
        is_twilight_owl = "is_twilight_owl" in request.form,
        is_eye_of_night = "is_eye_of_night" in request.form,
        is_T5 = "is_T5" in request.form,
        is_T6_2 = "is_T6_2" in request.form,
        is_T6_4 = "is_T6_4" in request.form,
        is_misery = "is_misery" in request.form,
        is_drums = "is_drums" in request.form,
        is_lust = "is_lust" in request.form,
        lust_count = "lust_count" in request.form)

        fight = Encounter(toon, buffs, int(request.form['fight_duration']))
        average_dps = fight.compute_dps(int(request.form['loop_count']))
        # app.logger.info('Simulation launched successfully')
        # return render_template('simulator/simulated.html', dps = average_dps)
        return render_template('simulator/index.html', 
            dps = average_dps, 
            toon = toon, 
            buffs = buffs,
            nb_loops = int(request.form['loop_count']),
            fight_duration = int(request.form['fight_duration']))
    return render_template('simulator/simulated.html')

#def get_simulation_result(id, check_author=True):
#    post = get_db().execute(
#        'SELECT p.id, title, body, created, author_id, username'
#        ' FROM post p JOIN user u ON p.author_id = u.id'
#        ' WHERE p.id = ?',
#        (id,)
#    ).fetchone()
#
#    if post is None:
#        abort(404, f"Post id {id} doesn't exist.")
#
#    if check_author and post['author_id'] != g.user['id']:
#        abort(403)
#
#    return render_template('simulator/index.html')
    
