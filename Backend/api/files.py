from flask import Blueprint, request, jsonify, send_file
from core.security import staff_or_admin_required, admin_required
from core.storage import (
    get_directory_contents,
    get_full_folder_tree,
    get_all_folders_list,
    save_uploaded_file,
    create_folder,
    delete_item,
    resolve_safe_path,
    clean_relative_path
)

files_bp = Blueprint("files", __name__)


def get_request_data():
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict() if request.form else {}


@files_bp.route("/folders", methods=["GET"])
@staff_or_admin_required
def list_all_folders():
    """
    Get flat list of all folders in the storage directory for selection dropdowns.
    """
    folders = get_all_folders_list()
    return jsonify({
        "success": True,
        "folders": folders
    }), 200


@files_bp.route("/files", methods=["GET"])
@staff_or_admin_required
def list_files():
    """
    List contents of a directory with breadcrumbs and rich metadata.
    Query params:
    - folder: relative directory path (default: root)
    - view: 'tree' for recursive legacy tree, otherwise structured folder list
    """
    view = request.args.get("view", "")
    if view == "tree":
        return jsonify(get_full_folder_tree()), 200

    folder = clean_relative_path(request.args.get("folder", ""))
    try:

        data = get_directory_contents(folder)
        return jsonify({"success": True, "data": data}), 200
    except FileNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to read folder: {e}"}), 500


@files_bp.route("/files/upload", methods=["POST"])
@admin_required
def upload_files():
    """
    Upload one or multiple files into a target directory.
    Form data:
    - folder: target directory relative path
    - file: single file or multiple files
    """
    cleaned_folder = clean_relative_path(request.form.get("folder", ""))

    uploaded = []
    files = request.files.getlist("file")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"success": False, "error": "No files selected for upload"}), 400

    for file_storage in files:
        if file_storage and file_storage.filename:
            try:
                info = save_uploaded_file(cleaned_folder, file_storage)
                uploaded.append(info)
            except ValueError as e:
                return jsonify({"success": False, "error": str(e)}), 400
            except Exception as e:
                return jsonify({"success": False, "error": f"Upload error: {e}"}), 500

    return jsonify({
        "success": True,
        "message": f"Successfully uploaded {len(uploaded)} file(s)",
        "files": uploaded
    }), 201


@files_bp.route("/files/folder", methods=["POST"])
@admin_required
def add_folder():
    """
    Create a new folder safely.
    Request body (JSON or Form):
    - parent_folder: parent directory path (default root)
    - folder_name: name of the new folder
    """
    data = get_request_data()
    parent = clean_relative_path(data.get("parent_folder", ""))
    name = str(data.get("folder_name", "") or "").strip()

    if not name:
        return jsonify({"success": False, "error": "Folder name is required"}), 400

    try:
        folder_info = create_folder(parent, name)
        return jsonify({
            "success": True,
            "message": f"Folder '{folder_info['name']}' created successfully",
            "folder": folder_info
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to create folder: {e}"}), 500


@files_bp.route("/files", methods=["DELETE"])
@admin_required
def remove_item():
    """
    Delete a specific file or entire folder.
    Accepts:
    - path: relative path to file or folder
    - OR folder + file combination (for legacy compatibility)
    """
    data = get_request_data()
    path = clean_relative_path(data.get("path", ""))

    if not path:
        folder = clean_relative_path(data.get("folder", ""))
        file_name = clean_relative_path(data.get("file", ""))
        path = "/".join(part for part in (folder, file_name) if part)

    if not path:
        return jsonify({"success": False, "error": "Path to delete is required"}), 400

    try:
        delete_item(path)
        return jsonify({"success": True, "message": f"Successfully deleted '{path}'"}), 200
    except FileNotFoundError:
        return jsonify({"success": False, "error": "Item not found"}), 404
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to delete item: {e}"}), 500


@files_bp.route("/files/download", methods=["GET"])
@staff_or_admin_required
def download_file():
    """
    Download or stream a file safely with proper MIME type.
    Query params:
    - path: relative file path inside STORAGE_DIR
    - download: 'true' to force attachment download, 'false' for in-browser view
    """
    path = clean_relative_path(request.args.get("path", ""))
    as_attachment = request.args.get("download", "false").lower() == "true"


    if not path:
        return jsonify({"success": False, "error": "File path is required"}), 400

    try:
        file_path = resolve_safe_path(path)
        if not file_path.exists() or file_path.is_dir():
            return jsonify({"success": False, "error": "File not found"}), 404

        return send_file(
            str(file_path),
            as_attachment=as_attachment,
            download_name=file_path.name
        )
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Error delivering file: {e}"}), 500
