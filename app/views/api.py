# Content DB
# Copyright (C) 2018  rubenwardy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from flask import *
from flask_user import *
from app import app
from app.models import *
from app.utils import is_package_page, rank_required
from .packages import QueryBuilder

@app.route("/api/packages/")
def api_packages_page():
	qb    = QueryBuilder()
	query = qb.buildPackageQuery()

	pkgs = [package.getAsDictionaryShort(app.config["BASE_URL"]) \
			for package in query.all() if package.getDownloadRelease() is not None]
	return jsonify(pkgs)

@app.route("/api/packages/<author>/<name>/")
@is_package_page
def api_package_page(package):
	return jsonify(package.getAsDictionary(app.config["BASE_URL"]))


@app.route("/api/topics/")
def api_topics_page():
	query = ForumTopic.query \
			.order_by(db.asc(ForumTopic.wip), db.asc(ForumTopic.name), db.asc(ForumTopic.title))
	pkgs = [t.getAsDictionary() for t in query.all()]
	return jsonify(pkgs)


@app.route("/api/topic_discard/", methods=["POST"])
@rank_required(UserRank.EDITOR)
def topic_set_discard():
	tid = request.args.get("tid")
	discard = request.args.get("discard")
	if tid is None or discard is None:
		abort(400)

	topic = ForumTopic.query.get(tid)
	topic.discarded = discard == "true"
	db.session.commit()

	return jsonify(topic.getAsDictionary())
