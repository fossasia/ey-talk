from django.urls import include, path
from django.views.generic.base import RedirectView

from pretalx.orga.views import (
    admin,
    auth,
    cards,
    cfp,
    dashboard,
    event,
    mails,
    organiser,
    person,
    plugins,
    review,
    schedule,
    speaker,
    submission,
    typeahead,
)

app_name = "orga"
urlpatterns = [
    path("login/", auth.LoginView.as_view(), name="login"),
    path("logout/", auth.logout_view, name="logout"),
    path("reset/", auth.ResetView.as_view(), name="auth.reset"),
    path("reset/<token>", auth.RecoverView.as_view(), name="auth.recover"),
    path("", RedirectView.as_view(url="event", permanent=False), name="base"),
    path("admin/", admin.AdminDashboard.as_view(), name="admin.dashboard"),
    path("admin/update/", admin.UpdateCheckView.as_view(), name="admin.update"),
    path(
        "admin/users/<slug:code>/",
        admin.AdminUserDetail.as_view(),
        name="admin.user.view",
    ),
    path(
        "admin/users/<slug:code>/delete/",
        admin.AdminUserDelete.as_view(),
        name="admin.user.delete",
    ),
    path("admin/users/", admin.AdminUserList.as_view(), name="admin.user.list"),
    path("me", event.UserSettings.as_view(), name="user.view"),
    path("me/subuser", person.SubuserView.as_view(), name="user.subuser"),
    path(
        "invitation/<code>",
        event.InvitationView.as_view(),
        name="invitation.view",
    ),
    path("start/redirect", dashboard.start_redirect_view, name="start.redirect"),
    path("start/", dashboard.StartView.as_view(), name="start"),
    path(
        "organiser/",
        dashboard.DashboardOrganiserListView.as_view(),
        name="organiser.list",
    ),
    path("organiser/new", organiser.OrganiserDetail.as_view(), name="organiser.create"),
    path(
        "organiser/<slug:organiser>/",
        include(
            [
                path(
                    "",
                    dashboard.DashboardOrganiserEventListView.as_view(),
                    name="organiser.dashboard",
                ),
                path(
                    "settings/",
                    organiser.OrganiserDetail.as_view(),
                    name="organiser.settings",
                ),
                path(
                    "settings/delete",
                    organiser.OrganiserDelete.as_view(),
                    name="organiser.delete",
                ),
                path(
                    "api/users", organiser.speaker_search, name="organiser.user_list"
                ),
                path("teams/", organiser.TeamList.as_view(), name="organiser.teams"),
                path(
                    "teams/new",
                    organiser.TeamDetail.as_view(),
                    name="organiser.teams.create",
                ),
                path(
                    "teams/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                organiser.TeamDetail.as_view(),
                                name="organiser.teams.view",
                            ),
                            path(
                                "delete",
                                organiser.TeamDelete.as_view(),
                                name="organiser.teams.delete",
                            ),
                            path(
                                "delete/<int:user_pk>",
                                organiser.TeamDelete.as_view(),
                                name="organiser.teams.delete_member",
                            ),
                            path(
                                "reset/<int:user_pk>",
                                organiser.TeamResetPassword.as_view(),
                                name="organiser.team.password_reset",
                            ),
                            path(
                                "uninvite",
                                organiser.TeamUninvite.as_view(),
                                name="organiser.teams.uninvite",
                            ),
                            path(
                                "resend",
                                organiser.TeamResend.as_view(),
                                name="organiser.teams.resend",
                            ),
                        ]
                    ),
                ),
                path(
                    "speakers/",
                    organiser.OrganiserSpeakerList.as_view(),
                    name="organiser.speakers",
                ),
            ]
        ),
    ),
    path("nav/typeahead/", typeahead.nav_typeahead, name="nav.typeahead"),
    path("event/new/", event.EventWizard.as_view(), name="event.create"),
    path("event/", dashboard.DashboardEventListView.as_view(), name="event.list"),
    path(
        "event/<slug:event>/",
        include(
            [
                path(
                    "", dashboard.EventDashboardView.as_view(), name="event.dashboard"
                ),
                path("login/", auth.LoginView.as_view(), name="event.login"),
                path("reset/", auth.ResetView.as_view(), name="event.auth.reset"),
                path(
                    "reset/<token>",
                    auth.RecoverView.as_view(),
                    name="event.auth.recover",
                ),
                path("delete", event.EventDelete.as_view(), name="event.delete"),
                path("live", event.EventLive.as_view(), name="event.live"),
                path("history/", event.EventHistory.as_view(), name="event.history"),
                path(
                    "cfp/",
                    RedirectView.as_view(pattern_name="orga:cfp.text.view"),
                    name="cfp",
                ),
                path("cfp/flow/", cfp.CfPFlowEditor.as_view(), name="cfp.flow"),
                path(
                    "cfp/questions/",
                    cfp.CfPQuestionList.as_view(),
                    name="cfp.questions.view",
                ),
                path(
                    "cfp/questions/new",
                    cfp.CfPQuestionDetail.as_view(),
                    name="cfp.questions.create",
                ),
                path(
                    "cfp/questions/remind",
                    cfp.CfPQuestionRemind.as_view(),
                    name="cfp.questions.remind",
                ),
                path(
                    "cfp/questions/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                cfp.CfPQuestionDetail.as_view(),
                                name="cfp.question.view",
                            ),
                            *cfp.QuestionOrderView.get_urls(),
                            path(
                                "delete",
                                cfp.CfPQuestionDelete.as_view(),
                                name="cfp.question.delete",
                            ),
                            path(
                                "edit",
                                cfp.CfPQuestionDetail.as_view(),
                                name="cfp.question.edit",
                            ),
                            path(
                                "toggle",
                                cfp.CfPQuestionToggle.as_view(),
                                name="cfp.question.toggle",
                            ),
                        ]
                    ),
                ),
                path("cfp/text", cfp.CfPTextDetail.as_view(), name="cfp.text.view"),
                path(
                    "cfp/types/",
                    cfp.SubmissionTypeList.as_view(),
                    name="cfp.types.view",
                ),
                path(
                    "cfp/types/new",
                    cfp.SubmissionTypeDetail.as_view(),
                    name="cfp.types.create",
                ),
                path(
                    "cfp/types/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                cfp.SubmissionTypeDetail.as_view(),
                                name="cfp.type.view",
                            ),
                            path(
                                "delete",
                                cfp.SubmissionTypeDelete.as_view(),
                                name="cfp.type.delete",
                            ),
                            path(
                                "default",
                                cfp.SubmissionTypeDefault.as_view(),
                                name="cfp.type.default",
                            ),
                        ]
                    ),
                ),
                path("cfp/tracks/", cfp.TrackList.as_view(), name="cfp.tracks.view"),
                path(
                    "cfp/tracks/new",
                    cfp.TrackDetail.as_view(),
                    name="cfp.track.create",
                ),
                path(
                    "cfp/tracks/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                cfp.TrackDetail.as_view(),
                                name="cfp.track.view",
                            ),
                            path(
                                "delete",
                                cfp.TrackDelete.as_view(),
                                name="cfp.track.delete",
                            ),
                            *cfp.TrackOrderView.get_urls(),
                        ]
                    ),
                ),
                path(
                    "cfp/access-codes/",
                    cfp.AccessCodeList.as_view(),
                    name="cfp.access_code.view",
                ),
                path(
                    "cfp/access-codes/new",
                    cfp.AccessCodeDetail.as_view(),
                    name="cfp.access_code.create",
                ),
                path(
                    "cfp/access-codes/<slug:code>/",
                    include(
                        [
                            path(
                                "",
                                cfp.AccessCodeDetail.as_view(),
                                name="cfp.access_code.view",
                            ),
                            path(
                                "send",
                                cfp.AccessCodeSend.as_view(),
                                name="cfp.access_code.send",
                            ),
                            path(
                                "delete",
                                cfp.AccessCodeDelete.as_view(),
                                name="cfp.access_code.delete",
                            ),
                        ]
                    ),
                ),
                path(
                    "mails/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                mails.MailDetail.as_view(),
                                name="mails.outbox.mail.view",
                            ),
                            path(
                                "copy",
                                mails.MailCopy.as_view(),
                                name="mails.outbox.mail.copy",
                            ),
                            path(
                                "delete",
                                mails.MailDelete.as_view(),
                                name="mails.outbox.mail.delete",
                            ),
                            path(
                                "send",
                                mails.OutboxSend.as_view(),
                                name="mails.outbox.mail.send",
                            ),
                            path(
                                "preview",
                                mails.MailPreview.as_view(),
                                name="mails.outbox.mail.preview",
                            ),
                        ]
                    ),
                ),
                path(
                    "mails/templates/",
                    mails.TemplateList.as_view(),
                    name="mails.templates.list",
                ),
                path(
                    "mails/templates/new",
                    mails.TemplateDetail.as_view(),
                    name="mails.templates.create",
                ),
                path(
                    "mails/templates/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                mails.TemplateDetail.as_view(),
                                name="mails.templates.view",
                            ),
                            path(
                                "delete",
                                mails.TemplateDelete.as_view(),
                                name="mails.templates.delete",
                            ),
                        ]
                    ),
                ),
                path(
                    "mails/compose/reminders",
                    mails.ComposeDraftReminders.as_view(),
                    name="mails.compose.draft_reminders",
                ),
                path(
                    "mails/compose",
                    mails.ComposeMailChoice.as_view(),
                    name="mails.compose.choose",
                ),
                path(
                    "mails/compose/teams/",
                    mails.ComposeTeamsMail.as_view(),
                    name="mails.compose.teams",
                ),
                path(
                    "mails/compose/sessions/",
                    mails.ComposeSessionMail.as_view(),
                    name="mails.compose.sessions",
                ),
                path("mails/sent", mails.SentMail.as_view(), name="mails.sent"),
                path(
                    "mails/outbox/",
                    mails.OutboxList.as_view(),
                    name="mails.outbox.list",
                ),
                path(
                    "mails/outbox/send",
                    mails.OutboxSend.as_view(),
                    name="mails.outbox.send",
                ),
                path(
                    "mails/outbox/purge",
                    mails.OutboxPurge.as_view(),
                    name="mails.outbox.purge",
                ),
                path(
                    "submissions/",
                    submission.SubmissionList.as_view(),
                    name="submissions.list",
                ),
                path(
                    "submissions/new",
                    submission.SubmissionContent.as_view(),
                    name="submissions.create",
                ),
                path(
                    "submissions/cards/",
                    cards.SubmissionCards.as_view(),
                    name="submissions.cards",
                ),
                path(
                    "submissions/feed/",
                    submission.SubmissionFeed(),
                    name="submissions.feed",
                ),
                path(
                    "submissions/apply-pending/",
                    submission.ApplyPending.as_view(),
                    name="submissions.apply_pending",
                ),
                path(
                    "submissions/statistics/",
                    submission.SubmissionStats.as_view(),
                    name="submissions.statistics",
                ),
                path(
                    "submissions/feedback/",
                    submission.AllFeedbacksList.as_view(),
                    name="submissions.feedback",
                ),
                path(
                    "submissions/tags/",
                    submission.TagList.as_view(),
                    name="submissions.tags.view",
                ),
                path(
                    "submissions/tags/new",
                    submission.TagDetail.as_view(),
                    name="submissions.tag.create",
                ),
                path(
                    "submissions/tags/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                submission.TagDetail.as_view(),
                                name="submissions.tag.view",
                            ),
                            path(
                                "delete",
                                submission.TagDelete.as_view(),
                                name="submissions.tag.delete",
                            ),
                        ]
                    ),
                ),
                path(
                    "submissions/<code>/",
                    include(
                        [
                            path(
                                "",
                                submission.SubmissionContent.as_view(),
                                name="submissions.content.view",
                            ),
                            path(
                                "submit",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.submit",
                            ),
                            path(
                                "accept",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.accept",
                            ),
                            path(
                                "reject",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.reject",
                            ),
                            path(
                                "confirm",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.confirm",
                            ),
                            path(
                                "withdraw",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.withdraw",
                            ),
                            path(
                                "delete",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.delete",
                            ),
                            path(
                                "cancel",
                                submission.SubmissionStateChange.as_view(),
                                name="submissions.cancel",
                            ),
                            path(
                                "speakers/",
                                submission.SubmissionSpeakers.as_view(),
                                name="submissions.speakers.view",
                            ),
                            path(
                                "speakers/add",
                                submission.SubmissionSpeakersAdd.as_view(),
                                name="submissions.speakers.add",
                            ),
                            path(
                                "speakers/delete",
                                submission.SubmissionSpeakersDelete.as_view(),
                                name="submissions.speakers.delete",
                            ),
                            path(
                                "reviews/",
                                review.ReviewSubmission.as_view(),
                                name="submissions.reviews",
                            ),
                            path(
                                "reviews/delete",
                                review.ReviewSubmissionDelete.as_view(),
                                name="submissions.reviews.submission.delete",
                            ),
                            path(
                                "feedback/",
                                submission.FeedbackList.as_view(),
                                name="submissions.feedback.list",
                            ),
                            path(
                                "toggle_featured",
                                submission.ToggleFeatured.as_view(),
                                name="submissions.toggle_featured",
                            ),
                            path(
                                "anonymise/",
                                submission.Anonymise.as_view(),
                                name="submissions.anonymise",
                            ),
                        ]
                    ),
                ),
                path("speakers/", speaker.SpeakerList.as_view(), name="speakers.list"),
                path(
                    "speakers/export/",
                    speaker.SpeakerExport.as_view(),
                    name="speakers.export",
                ),
                path(
                    "speakers/<code>/",
                    include(
                        [
                            path(
                                "",
                                speaker.SpeakerDetail.as_view(),
                                name="speakers.view",
                            ),
                            path(
                                "reset",
                                speaker.SpeakerPasswordReset.as_view(),
                                name="speakers.reset",
                            ),
                            path(
                                "toggle-arrived",
                                speaker.SpeakerToggleArrived.as_view(),
                                name="speakers.arrived",
                            ),
                        ]
                    ),
                ),
                path(
                    "info/",
                    speaker.InformationList.as_view(),
                    name="speakers.information.list",
                ),
                path(
                    "info/new",
                    speaker.InformationDetail.as_view(),
                    name="speakers.information.create",
                ),
                path(
                    "info/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                speaker.InformationDetail.as_view(),
                                name="speakers.information.view",
                            ),
                            path(
                                "delete",
                                speaker.InformationDelete.as_view(),
                                name="speakers.information.delete",
                            ),
                        ]
                    ),
                ),
                path(
                    "reviews/",
                    review.ReviewDashboard.as_view(),
                    name="reviews.dashboard",
                ),
                path(
                    "reviews/bulk/",
                    review.BulkReview.as_view(),
                    name="reviews.bulk",
                ),
                path(
                    "reviews/regenerate/",
                    review.RegenerateDecisionMails.as_view(),
                    name="reviews.regenerate",
                ),
                path(
                    "reviews/assign/import",
                    review.ReviewAssignmentImport.as_view(),
                    name="reviews.assign.import",
                ),
                path(
                    "reviews/assign/",
                    review.ReviewAssignment.as_view(),
                    name="reviews.assign",
                ),
                path(
                    "reviews/export/",
                    review.ReviewExport.as_view(),
                    name="reviews.export",
                ),
                path(
                    "settings/",
                    event.EventDetail.as_view(),
                    name="settings.event.view",
                ),
                path(
                    "settings/mail",
                    event.EventMailSettings.as_view(),
                    name="settings.mail.view",
                ),
                path(
                    "settings/plugins",
                    plugins.EventPluginsView.as_view(),
                    name="settings.plugins.select",
                ),
                path(
                    "settings/widget",
                    event.WidgetSettings.as_view(),
                    name="settings.widget",
                ),
                path(
                    "settings/review/",
                    event.EventReviewSettings.as_view(),
                    name="settings.review",
                ),
                path(
                    "settings/review/phase/<int:pk>/",
                    include(
                        [
                            *event.ReviewPhaseOrderView.get_urls(),
                            path(
                                "activate",
                                event.PhaseActivate.as_view(),
                                name="settings.review.phase.activate",
                            ),
                        ]
                    ),
                ),
                path(
                    "schedule/", schedule.ScheduleView.as_view(), name="schedule.main"
                ),
                path(
                    "schedule/export/",
                    schedule.ScheduleExportView.as_view(),
                    name="schedule.export",
                ),
                path(
                    "schedule/export/trigger",
                    schedule.ScheduleExportTriggerView.as_view(),
                    name="schedule.export.trigger",
                ),
                path(
                    "schedule/export/download",
                    schedule.ScheduleExportDownloadView.as_view(),
                    name="schedule.export.download",
                ),
                path(
                    "schedule/release",
                    schedule.ScheduleReleaseView.as_view(),
                    name="schedule.release",
                ),
                path(
                    "schedule/quick/<code>/",
                    schedule.QuickScheduleView.as_view(),
                    name="schedule.quick",
                ),
                path(
                    "schedule/reset",
                    schedule.ScheduleResetView.as_view(),
                    name="schedule.reset",
                ),
                path(
                    "schedule/toggle",
                    schedule.ScheduleToggleView.as_view(),
                    name="schedule.toggle",
                ),
                path(
                    "schedule/resend_mails",
                    schedule.ScheduleResendMailsView.as_view(),
                    name="schedule.resend_mails",
                ),
                path(
                    "schedule/rooms/",
                    schedule.RoomList.as_view(),
                    name="schedule.rooms.list",
                ),
                path(
                    "schedule/rooms/new",
                    schedule.RoomDetail.as_view(),
                    name="schedule.rooms.create",
                ),
                path(
                    "schedule/rooms/<int:pk>/",
                    include(
                        [
                            path(
                                "",
                                schedule.RoomDetail.as_view(),
                                name="schedule.rooms.view",
                            ),
                            path(
                                "delete",
                                schedule.RoomDelete.as_view(),
                                name="schedule.rooms.delete",
                            ),
                            *schedule.RoomOrderView.get_urls(),
                        ]
                    ),
                ),
                path(
                    "schedule/api/talks/<int:pk>/",
                    schedule.TalkUpdate.as_view(),
                    name="schedule.api.update",
                ),
                path(
                    "schedule/api/talks/",
                    schedule.TalkList.as_view(),
                    name="schedule.api.talks",
                ),
                path(
                    "schedule/api/availabilities/",
                    schedule.ScheduleAvailabilities.as_view(),
                    name="schedule.api.availabilities",
                ),
                path(
                    "schedule/api/warnings/",
                    schedule.ScheduleWarnings.as_view(),
                    name="schedule.api.warnings",
                ),
            ]
        ),
    ),
]
