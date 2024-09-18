from unittest.mock import patch

from django_kafka.models import KafkaSkipMixin
from django_kafka.tests.models import AbstractModelTestCase


class KafkaSkipModelTestCase(AbstractModelTestCase):
    abstract_model = KafkaSkipMixin

    @patch("django_kafka.models.super")
    def test_save_update_fields_not_in_kwargs(self, super_mock):
        """
        kafka_skip should be set to False when update_fields is not provided
        """

        instance = self.model(pk=1, kafka_skip=True)

        instance.save()

        # save sets kafka_skip value to False
        self.assertFalse(instance.kafka_skip)
        # didn't forget to call super
        super_mock.assert_called_once_with()
        # no update_fields set
        super_mock.return_value.save.assert_called_once_with(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    @patch("django_kafka.models.super")
    def test_save_update_fields_in_kwargs_without_kafka_skip(self, super_mock):
        """
        kafka_skip should be set to False when update_fields does not contain kafka_skip
        """
        instance = self.model(pk=1, kafka_skip=True)

        update_fields = ["some_fields"]

        instance.save(update_fields=update_fields)

        # save sets kafka_skip value to False
        self.assertFalse(instance.kafka_skip)
        # didn't forget to call super
        super_mock.assert_called_once_with()
        # kafka_skip added to update_fields
        super_mock.return_value.save.assert_called_once_with(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=["kafka_skip", *update_fields],
        )

    @patch("django_kafka.models.super")
    def test_save_update_fields_in_kwargs_with_kafka_skip(self, super_mock):
        """
        kafka_skip should not be changed if provided in update_fields
        """
        update_fields = ["some_field", "kafka_skip"]

        instance = self.model(pk=1, kafka_skip=True)

        instance.save(update_fields=update_fields)

        # save does not change kafka_skip value
        self.assertTrue(instance.kafka_skip)
        # didn't forget to call super
        super_mock.assert_called_once_with()
        # update_fields are not changed
        super_mock.return_value.save.assert_called_once_with(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=update_fields,
        )

    @patch("django_kafka.models.super")
    def test_queryset_update_sets_kafka_skip(self, super_mock):
        """
        `update` method should automatically set `kafka_skip=False`
          if `kafka_skip` is not provided in kwargs.
        """
        # update_kwargs does not contain kafka_skip
        update_kwargs = {"some_field": "some_value"}

        self.model.objects.update(**update_kwargs)

        # kafka_skip=False was added to the update_kwargs
        super_mock.return_value.update.assert_called_once_with(
            **{"kafka_skip": False, **update_kwargs},
        )

    @patch("django_kafka.models.super")
    def test_queryset_update_does_not_override_kafka_skip(self, super_mock):
        """
        `update` method should not change `kafka_skip`
          if `kafka_skip` is provided in kwargs
        """
        # update_kwargs contains kafka_skip
        update_kwargs = {"kafka_skip": True, "some_field": "some_value"}

        self.model.objects.update(**update_kwargs)

        # kafka_skip is not changed, update_kwargs are not changed
        super_mock.return_value.update.assert_called_once_with(**update_kwargs)
