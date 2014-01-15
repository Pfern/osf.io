<%inherit file="project/addon/settings.mako" />

<div class="form-group">
	%if node_auth:

    		<label for="s3Addon">Access Key</label>
    		<input class="form-control" id="secret_key" name="secret_key" value="${access_key}" disabled />
    		 <br>
        	<a id="s3DelKey" class="btn btn-danger">Delete Access Key</a>
	%else:
        <a id="s3createKey" class="btn btn-primary  ${'' if user_has_auth else 'disabled'}">
        	Create Access Key
        </a>

    %endif
</div>

<br>

<div class="form-group">
    <label for="githubRepo">Bucket Name</label>
    <input class="form-control" id="s3_bucket" name="s3_bucket" value="${s3_bucket}" ${'disabled' if not node_auth else ''} />
</div>

<script type="text/javascript">

    $(document).ready(function() {

        $('#s3createKey').on('click', function() {
                $.ajax({
                    type: 'POST',
                    url: nodeApiUrl + 's3/makeKey/',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(response) {
                        window.location.reload();
                    }
                });
        });

        $('#s3DelKey').on('click', function() {
            bootbox.confirm(
                'Are you sure you want to delete your Amazon S3 access key?',
                function(result) {
                    if (result) {
                        $.ajax({
                            url: nodeApiUrl + 's3/key/delete/',
                            type: 'POST',
                            contentType: 'application/json',
                            dataType: 'json',
                            success: function() {
                                window.location.reload();
                            }
                        });
                    }
                }
            )
        });
    });

</script>
