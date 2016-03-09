/**
 * New and Noteworthy Projects
 */

var $ = require('jquery');
var m = require('mithril');
var $osf = require('js/osfHelpers');
var Raven = require('raven-js');

// CSS
require('css/quick-project-search-plugin.css');

// XHR config for apiserver connection
var xhrconfig = function(xhr) {
    xhr.withCredentials = true;
};


var NewAndNoteworthy = {
    controller: function() {
        var self = this;
        self.newAndNoteworthyNodes = m.prop([]); // New and noteworthy nodes list
        self.popularNodes = m.prop([]); // Most popular nodes list
        self.contributorsMapping = {}; // Dictionary mapping node id to some of the contrib names and the contrib total.
        self.SHOW_TOTAL = 5; // Number of new and noteworthy projects displayed in each column
        self.errorLoading = m.prop(false);  // True if error retrieving projects or contributors.
        self.someDataLoaded = m.prop(false); // True when the initial request to retrieve projects is complete.

        // Switches errorLoading to true
        self.requestError = function(result){
            self.errorLoading = m.prop(true);
            Raven.captureMessage('Error loading new and noteworthy projects on home page.', {requestReturn: result});
        };

        // Load new and noteworthy nodes
        var newAndNoteworthyUrl = $osf.apiV2Url('nodes/' + window.contextVars.newAndNoteworthy + '/node_links/', {});
        var newAndNoteworthyPromise = m.request({method: 'GET', url: newAndNoteworthyUrl, config: xhrconfig, background: true});
        newAndNoteworthyPromise.then(function(result){
            var numNew = Math.min(result.data.length, self.SHOW_TOTAL);
            for (var l = 0; l < numNew; l++) {
                self.newAndNoteworthyNodes().push(result.data[l]);
                self.fetchContributors(result.data[l]);
            }
            self.someDataLoaded(true);
        }, function _error(result){
            self.requestError(result);
        });

        // Load popular nodes
        var popularUrl = $osf.apiV2Url('nodes/' + window.contextVars.popular + '/node_links/', {});
        var popularPromise = m.request({method: 'GET', url: popularUrl, config: xhrconfig, background: true});
        popularPromise.then(function(result){
            var numPopular = Math.min(result.data.length, self.SHOW_TOTAL);
            for (var l = 0; l < numPopular; l++) {
                self.popularNodes().push(result.data[l]);
                self.fetchContributors(result.data[l]);
            }
            self.someDataLoaded(true);
        }, function _error(result){
            self.requestError(result);
        });

        // Additional API call to fetch node link contributors
        self.fetchContributors = function(nodeLink) {
            var url = nodeLink.embeds.target_node.data.relationships.contributors.links.related.href;
            var promise = m.request({method: 'GET', url : url, config: xhrconfig});
            promise.then(function(result){
                var contribNames = [];
                result.data.forEach(function (contrib){
                    contribNames.push($osf.findContribName(contrib.embeds.users.data.attributes));
                });
                var numContrib = result.links.meta.total;
                var nodeId = nodeLink.id;
                self.contributorsMapping[nodeId] = [contribNames, numContrib];
            }, function _error(result){
                self.requestError(result);
            });
        };

        // Gets contrib family name for display
        self.getFamilyName = function(i, node) {
            return self.contributorsMapping[node.id][0][i];
        };

        self.addToolTip = function(line) {
            var $line = $(line);
            if (line.offsetWidth < line.scrollWidth) {
                $line.tooltip('show');
            }
        };
    },
    view : function(ctrl) {
        if (ctrl.errorLoading()) {
            return m('p.text-center.m-v-lg', 'Error loading projects. Please refresh the page.');
        }

        if (!ctrl.someDataLoaded()) {
            return m('.text-center', m('.logo-spin.logo-xl.m-v-xl'));
        }

        function nodeDisplay(node) {
            var description = node.embeds.target_node.data.attributes.description;
            var title = node.embeds.target_node.data.attributes.title;
            var contributors = $osf.contribNameFormat(node, ctrl.contributorsMapping[node.id][1], ctrl.getFamilyName);
            var destination = '/' + node.embeds.target_node.data.id;

            return m('.public-projects-item', {onclick: function(){
                location.href = destination;
            }},[
                m('h5', m('a', {href: destination}, title)),
                m('span.prevent-overflow',  {'data-title': contributors, 'data-location': 'top', onmouseover: function() {
                    ctrl.addToolTip(this);
                }}, m('i', 'by ' + contributors)),
                description ? m('p.prevent-overflow', {'data-title': description, 'data-location': 'top', onmouseover: function(){
                    ctrl.addToolTip(this);
                }}, description) : ''

            ]);
        }

        function newAndNoteworthyProjectsTemplate () {
            return ctrl.newAndNoteworthyNodes().map(function(node){
                return nodeDisplay(node);
            });
        }

        function popularProjectsTemplate () {
            return ctrl.popularNodes().map(function(node){
                return nodeDisplay(node);
            });
        }

        function findMoreProjectsButton () {
            return m('a.btn.btn-default.m-v-lg', {type:'button', href:'/search'}, 'Find more projects with advanced search');
        }


        return m('',[
            m('.row',[
                m('.col-xs-12.col-md-6', m('.public-projects-box.', m('h4.m-b-md','New and Noteworthy'), newAndNoteworthyProjectsTemplate())),
                m('.col-xs-12.col-md-6', m('.public-projects-box.', m('h4.m-b-md','Most Popular'), popularProjectsTemplate ()))
            ]),
            m('.row', m('.text-center.col-sm-12', findMoreProjectsButton()))
        ]);
    }
};

module.exports = NewAndNoteworthy;

